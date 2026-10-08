from dataclasses import dataclass
from enum import Enum
import json
import time
from typing import List
import threading
import websocket
import signal
import serial
import struct
import os
import tomllib
import copy

constants = {}
# FIXME this is code from STORM 2026, so we need to refactor/rebase it

# ---------- Helpers ----------
def clamp(value, min_val=-1.0, max_val=1.0):
    return max(min_val, min(max_val, value))


def apply_deadzone(v, dz):
    return 0.0 if abs(v) < dz else v


def normalize_wheels(wheels: List[float]) -> List[float]:
    m = max(abs(w) for w in wheels)
    return [w / m for w in wheels] if m > 1.0 else wheels


def square_inputs(val: float) -> float:
    sign = -1 if val < 0 else 1
    return sign * (val ** 2)


def mecanum_blend(x: float, y: float, w: float) -> List[float]:
    vx = clamp(apply_deadzone(square_inputs(x), constants["DEADZONE"]), -0.7, 0.7)  # forward/back
    vy = clamp(apply_deadzone(square_inputs(y), constants["DEADZONE"]), -0.7, 0.7)  # strafe right-left
    omega = clamp(apply_deadzone(square_inputs(w), constants["DEADZONE"]), -0.7, 0.7)  # turn

    vx /= 2
    vy /= 2
    omega /= 2

    fl = vx + vy + omega
    fr = vx - vy - omega
    bl = vx - vy + omega
    br = vx + vy - omega
    return normalize_wheels([-fl, fr, -bl, br])  # left are negative because motors are reversed


# ---------- Robot command struct (Pi -> Pico) ----------
# needs to be between 0 and 255. assumes speed is a signed percentage float.
def scale_motor_speed(speed: float) -> int:
    return int(127 * speed) + 127


# needs to be between 0 and 255. assumes pos is degrees.
def scale_servo_pos(pos: float) -> int:
    return int(pos * 255)  # FIXME do I need a 360 or 2pi somewhere in here???


# FIXME are these good default values?
@dataclass
class RobotCommand:
    left_front_drive_motor: float = 0.0
    left_back_drive_motor: float = 0.0
    right_front_drive_motor: float = 0.0
    right_back_drive_motor: float = 0.0

    intake_motor: float = 0.0

    climb_motor_speed: float = 0.0

    connected: bool = False  # for loss-of-signal


@dataclass
class ControllerState:
    left_stick_x: float = 0.0
    left_stick_y: float = 0.0
    right_stick_x: float = 0.0
    right_stick_y: float = 0.0

    left_stick_button: bool = False
    right_stick_button: bool = False

    button_b: bool = False
    button_x: bool = False
    button_y: bool = False

    left_bumper: bool = False
    right_bumper: bool = False

    dpad_top: bool = False
    dpad_bottom: bool = False
    dpad_left: bool = False
    dpad_right: bool = False

    trigger_left: float = 0.0
    trigger_right: float = 0.0


class TimedRobotCommand:
    def __init__(self, command: RobotCommand, timeout: float):
        self.command = command
        self.timeout = timeout

        self.time = -1

    def start(self):
        self.time = time.time()

    def is_done(self) -> bool:
        if (time.time() - self.time) > self.timeout:
            return True
        return False


class AutonomousSequence:
    def __init__(self, commands: List[TimedRobotCommand]):
        self.commands = commands
        self.index = 0

        self.started = False

    def start(self):
        self.index = 0
        self.commands[self.index].start()

        self.started = True

    def run(self) -> TimedRobotCommand:
        try:
            if self.commands[self.index].is_done():
                self.index += 1

            # if self.index >= (len(self.commands)+1):
            #     return None

            if self.commands[self.index].time == -1:
                self.commands[self.index].start()
        except Exception as e:
            return None

        return self.commands[self.index]


class RobotState(Enum):
    OFF = 0
    AUTONOMOUS = 1
    TELEOP = 2
    TEST = 3


# ======== Autonomous Programs ========
def get_autonomous_programs():
    driveForwards = RobotCommand()
    driveForwards.left_front_drive_motor, \
        driveForwards.right_front_drive_motor, \
        driveForwards.left_back_drive_motor, \
        driveForwards.right_back_drive_motor = mecanum_blend(0.7, 0.0, 0.0)

    DriveForwardAutonomous = AutonomousSequence([
        TimedRobotCommand(driveForwards, 4.0),  # 5 seconds
        TimedRobotCommand(RobotCommand(), 2)  # and stop?
    ])

    ScoreOneAutonomous = AutonomousSequence([
        TimedRobotCommand(driveForwards, 5.0),  # position ourselves
        TimedRobotCommand(RobotCommand(), 2),  # stop
    ])

    return [DriveForwardAutonomous, ScoreOneAutonomous]


# =====================================

# generate serial message to be sent to Pico
def pack_robot_command(cmd: RobotCommand) -> bytes:
    # okay so this is assuming we're doing a mega-message and not variable-size messages
    # so no COMMAND bytes, but keeping the start and end bytes

    # FIXME is it supposed to be little or big endian?
    msg = struct.pack(
        ">c12Bc",
        bytes(constants["START_BYTE"], 'ascii'),
        scale_motor_speed(cmd.left_front_drive_motor),
        scale_motor_speed(cmd.left_back_drive_motor),
        scale_motor_speed(cmd.right_front_drive_motor),
        scale_motor_speed(cmd.right_back_drive_motor),
        scale_motor_speed(cmd.intake_motor),
        scale_motor_speed(cmd.climb_motor_speed),
        cmd.connected,
        bytes(constants["END_BYTE"], 'ascii')
    )

    return msg


# ---------- Robot control client ----------
class RobotClient:
    def __init__(self, server_url, default_command: RobotCommand, autos: List[AutonomousSequence]):
        self.ws = websocket.WebSocketApp(
            server_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error
        )
        self.connected_ws = False

        self.lock = threading.Lock()
        self.stop_event = threading.Event()

        self.controller_state = ControllerState()
        self.last_controller_state = ControllerState()

        self.arm_poses = [constants["ARM_BASE_PICK"], constants["ARM_BASE_STOW"], constants["ARM_BASE_LOW"],
                          constants["ARM_BASE_HIGH"], constants["ARM_BASE_CLIMB"]]

        self.default_command = default_command
        self.robot_cmd = default_command
        self.robot_state = RobotState.TELEOP

        camera_x_diff = 0.0
        camera_y_diff = 0.0
        camera_rot = 0.0

        self.autonomous_programs = autos
        self.auto_idx = 0  # FIXME?

        # TODO FIXME have a callback to check FMS periodically? or like... idk man...

        # try to open serial connection to Pico
        self.try_open_serial()

    def try_open_serial(self):
        try:
            self.serial = serial.Serial(constants["SERIAL_PORT"], constants["BAUD_RATE"], timeout=0.5)
            print(f"[Robot] Serial connected on {constants["SERIAL_PORT"]}")
        except Exception as e:
            self.serial = None
            print(f"[Robot] Serial open failed: {e}")

    # --- WebSocket callbacks ---
    def on_open(self, ws):
        print("[Robot] WS connected")

        # send websocket message so the relay server knows where to find us
        ws.send(json.dumps({
            "sender": constants["ROBOT_NAME"],
            "destination": constants["CONTROLLER_INPUT_NAME"],  # FIXME???
            "data": "{}"
        }))

        self.connected_ws = True

    def on_message(self, ws, raw):
        try:
            msg = json.loads(raw)
            if msg.get("destination") != constants["ROBOT_NAME"]:
                return

            payload = json.loads(msg["data"])
            msg_id = payload.get("id")

            # TODO FIXME separate one for autonomous???

            # update robot state
            # if msg_id == 30 and msg.get("sender") == constants["GUI_NAME"]:
            #    with self.lock:
            #        self.robot_state = payload.get("state")
            # FIXME autonomous program selector
            if msg_id == 6767:
                with self.lock:
                    self.robot_state = RobotState.AUTONOMOUS

            # update controller state for robot control
            elif msg_id == 10 and msg.get("sender") == constants["CONTROLLER_INPUT_NAME"]:
                with self.lock:
                    self.controller_state.left_stick_x = payload.get("left_stick_x")
                    self.controller_state.left_stick_y = payload.get("left_stick_y")
                    self.controller_state.right_stick_x = payload.get("right_stick_x")
                    self.controller_state.right_stick_y = payload.get("right_stick_y")
                    self.controller_state.left_stick_button = payload.get("left_stick_button")
                    self.controller_state.right_stick_button = payload.get("right_stick_button")
                    self.controller_state.button_b = payload.get("button_b")
                    self.controller_state.button_x = payload.get("button_x")
                    self.controller_state.button_y = payload.get("button_y")
                    self.controller_state.left_bumper = payload.get("button_left_bumper")
                    self.controller_state.right_bumper = payload.get("button_right_bumper")
                    self.controller_state.dpad_top = payload.get("dpad_top")
                    self.controller_state.dpad_bottom = payload.get("dpad_bottom")
                    self.controller_state.dpad_left = payload.get("dpad_left")
                    self.controller_state.dpad_right = payload.get("dpad_right")
                    self.controller_state.trigger_left = payload.get("trigger_left")
                    self.controller_state.trigger_right = payload.get("trigger_right")

            # update robot position/alignment from AprilTag process
            elif msg_id == 141 and msg.get("sender") == constants["APRILTAG_NAME"]:
                with self.lock:
                    self.tag_id = payload.get("ids")
                    self.field_x = payload.get("x")
                    self.field_y = payload.get("y")
                    self.field_heading = payload.get("heading")
                    self.camera_x_diff = payload.get("x_diff")
                    self.camera_y_diff = payload.get("y_diff")
                    self.camera_rot = payload.get("rot")

        except Exception as e:
            print(f"[Robot] WS message error: {e}")

    def on_close(self, ws, code, reason):
        print("[Robot] WS closed:", code, reason)

        # TODO: send a 'kill everything' message to robot?

        self.connected_ws = False
        self.stop_event.set()

    def on_error(self, ws, error):
        print("[Robot] WS error:", error)

    # --- Mapping from controller -> robot_cmd ---
    def update_robot_command_from_controller(self):
        s = self.controller_state
        cmd = self.robot_cmd

        # Drive (mecanum)
        cmd.left_front_drive_motor, \
            cmd.right_front_drive_motor, \
            cmd.left_back_drive_motor, \
            cmd.right_back_drive_motor = mecanum_blend(s.left_stick_y, s.left_stick_x, s.right_stick_x)

        # Auto alignment: right stick button hold
        if s.right_stick_button:
            rot_dir = 0
            hor_amt = 0
            dep_amt = 0

            # Rotate to face tag
            if not abs(self.camera_rot) > 3:

                cmd.left_front_drive_motor, \
                    cmd.right_front_drive_motor, \
                    cmd.left_back_drive_motor, \
                    cmd.right_back_drive_motor = mecanum_blend(s.left_stick_y, s.left_stick_x, rot_dir)  ###
                if self.camera_rot < -3:
                    rot_dir = 0.2  # Change this to be more real rotation (idk what good numbers are)
                elif self.camera_rot > 3:
                    rot_dir = -0.2  # Change this to be more real rotation (idk what good numbers are)
                else:
                    rot_dir = 0

            # Center to tag
            if not abs(self.camera_x_diff) > 0.5:
                cmd.left_front_drive_motor, \
                    cmd.right_front_drive_motor, \
                    cmd.left_back_drive_motor, \
                    cmd.right_back_drive_motor = mecanum_blend(s.left_stick_y, hor_amt, s.right_stick_x)  ###
                if self.camera_x_diff > 0.5:
                    hor_amt = 0.2  # Change this to be more real translation (idk what good numbers are)
                elif self.camera_x_diff < -0.5:
                    hor_amt = -0.2  # Change this to be more real translation (idk what good numbers are)
                else:
                    hor_amt = 0

            # Depth Alignment
            if not abs(self.camera_y_diff) > 17.5:
                cmd.left_front_drive_motor, \
                    cmd.right_front_drive_motor, \
                    cmd.left_back_drive_motor, \
                    cmd.right_back_drive_motor = mecanum_blend(dep_amt, s.left_stick_x, s.right_stick_x)
                if self.camera_y_diff < 17.5:
                    dep_amt = -0.2  # Change this to be more real translation (idk what good numbers are)
                elif self.camera_y_diff > 17.5:
                    dep_amt = 0.2  # Change this to be more real translation (idk what good numbers are)
                else:
                    dep_amt = 0

        # Intake: right bumper in, left bumper out
        if s.right_bumper:
            cmd.intake_motor = constants["INTAKE_IN_SPEED"]
        elif s.left_bumper:
            cmd.intake_motor = constants["INTAKE_OUT_SPEED"]
        else:
            cmd.intake_motor = 0.0

        # Climber retract/extend
        cmd.climb_motor_speed = s.trigger_left - s.trigger_right

        # loss of signal checkb
        cmd.connected = self.connected_ws

        self.robot_cmd = cmd
        self.last_controller_state = copy.copy(s)

    def update_robot_command_from_autonomous(self):
        if not self.autonomous_programs[self.auto_idx].started:
            self.autonomous_programs[self.auto_idx].start()

        auto_cmd = self.autonomous_programs[self.auto_idx].run()
        if auto_cmd is not None:
            self.robot_cmd = auto_cmd.command
            return auto_cmd.command
        else:
            return None

    def serial_loop(self):
        while not self.stop_event.is_set():
            cmd = RobotCommand()

            with self.lock:
                if self.robot_state == RobotState.OFF:
                    pass  # FIXME send like, default command? or no command?

                elif self.robot_state == RobotState.AUTONOMOUS:
                    print(self.robot_cmd)

                    if self.update_robot_command_from_autonomous() is None:
                        print("SWITCHING TO T")
                        self.robot_state = RobotState.TELEOP
                    else:
                        if self.robot_cmd is not None:
                            cmd = self.robot_cmd
                            cmd.connected = self.connected_ws

                elif self.robot_state == RobotState.TELEOP:
                    self.update_robot_command_from_controller()
                    cmd = self.robot_cmd

            time.sleep(1.0 / constants["UPDATE_HZ"])

    def shutdown(self, *_):
        print("\n[Robot] Shutting down...")
        self.stop_event.set()
        try:
            self.ws.close()
        except:
            pass
        if self.serial and self.serial.is_open:
            self.serial.close()

    def run(self):
        t = threading.Thread(target=self.serial_loop, daemon=True)
        t.start()
        print(print(f"Starting robot code with ID: {t.native_id}"))
        signal.signal(signal.SIGINT, self.shutdown)

        self.ws.run_forever(ping_interval=10, ping_timeout=5)


# ---------- Main ----------
if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Tip: for serial, add your user to 'dialout' or run with sudo.")

    with open("../constants.toml", "rb") as const_file:
        try:
            constants = tomllib.load(const_file)
        except Exception as e:
            print("[Robot] Failed to read constants file")
            raise SystemExit

    # have to update this after reading the constants file
    default_robot_command = RobotCommand()

    url = constants["COMPETITION_SERVER_URL"] if constants["COMPETITION"] else constants["LOCAL_SERVER_URL"]
    port = constants["COMPETITION_SERVER_PORT"] if constants["COMPETITION"] else constants["LOCAL_SERVER_PORT"]

    robot = RobotClient(f"{url}:{port}", default_robot_command, get_autonomous_programs(constants))

    try:
        robot.run()
    except KeyboardInterrupt:
        pass

    robot.shutdown()