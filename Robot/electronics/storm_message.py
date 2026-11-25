# TODO standard file header

"""
This Python file is based on the Arduino/C++ StormMessage.hpp in the firmware folder.
That is considered the reference implementation of StormLib, so if something doesn't match,
update this file to match the C++ one.

Link to serial specification: TODO
"""

from enum import Enum, unique
import struct
from typing import List


# some values we will need to know when converting the messages into actual bytes
MAX_INT16 = 32767
MAX_UINT16 = 65535
MAX_INT8 = 128
MAX_UINT8 = 255

#TODO: docstring
def float_to_int16(x: float) -> int:
    # scale up to size
    x *= MAX_INT16

    # move to the middle
    x += MAX_INT16

    return int(x)

#TODO: docstring
def float_to_uint16(x: float) -> int:
    # take the abs
    x = abs(x)

    # scale up to size
    x *= MAX_UINT16

    return int(x)


@unique
class StormAddress(Enum):
    """Unique identifier indicating who the message is for
    Only the computer (address 1) can send messages on its own initiative.
    The special address 0 indicates the message is for all boards (e.x. heartbeat).
    """
    ALL = 0
    COMPUTER = 1
    TRAVERSAL = 2
    CANNON = 3
    NONE = 4


@unique
class StormMessageId(Enum):
    """The unique message ID of the message, as defined in the STORM 2027 Serial Specification.
    """
    # protocol messages
    ComputerRequestMsg = 10
    HeartbeatMsg = 11
    ConfigurationCmd = 12
    ConfigurationCompleteMsg = 13

    # Traversal board messages
    RobotVelocityCmd = 20
    DriveVelocitiesCmd = 21
    DriveVoltageCmd = 22
    DriveRawCmd = 23
    DriveFeedbackRsp = 24
    BatteryVoltageRsp = 25

    ClimberHeightCmd = 26
    ClimberVelocityCmd = 27
    ClimberRawCmd = 28
    ClimberPositionCmd = 29
    ClimberSensorRsp = 30
    ClimberStateRsp = 31

    # Cannon board messages
    ShooterVelocityCmd = 50
    ShooterRawCmd = 51
    ShooterPositionCmd = 52
    ShooterStateRsp = 53

    IndexerVelocityCmd = 54
    IndexerRawCmd = 55
    IndexerFeedCmd = 56
    IntakeVelocityCmd = 57
    IntakeFeedCmd = 58
    IntakeRawCmd = 59
    IntakeIndexerRsp = 60

    # this is special and used for testing only
    DebugeMsg = 255



# TODO docstring
class StormMessage:
    START_BYTE = 0xAA
    END_BYTE = 0xFF

    def __init__(self, address: StormAddress, id: StormMessageId):
        # TODO docstring
        self.address = address
        self.id = id

        self.data = [] # this will be set by subclasses
        self.pack_string = ""  # defines how self.data is supposed to get struct.pack()ed

        # little-endian character for struct.pack
        self.endianness = "<"

    def __repr__(self) -> str:
        #TODO docstring
        #TODO maybe this could be better
        return f"{self.START_BYTE} {self.address} {self.id} size??? {self.data} {self.END_BYTE}"

    def pack(self) -> bytes:
        # TODO docstring

        # subclasses set the pack string and data, so they don't have to override this method
        # because the rest of the message format doesn't (well, *shouldn't*) change.
        data_bytes = struct.pack(self.endianness + self.pack_string, *self.data)

        # need to pack just the data first so we can calulate size
        # we *could* let subclasses specify that, but that would be more error-prone
        size = len(data_bytes)
        
        # pack the whole message now
        packed_msg = struct.pack(
            self.endianness + "",
            self.START_BYTE,
            self.address,
            size,
            data_bytes,
            self.END_BYTE
        )
        
        return packed_msg

# ==============================================
# ===   start message subclass definitions   ===
# ==============================================

#ID 10
#TODO FIXME rename this ????
class Request(StormMessage):
    def __init__(self, addressed_to: StormAddress, request_id: StormMessageId):
        super().__init__(addressed_to, StormMessageId.ComputerRequestMsg)
                
        self.data = [request_id]
        self.pack_string = "B" # unsigned char (uint8_t)

# ID 11
class HeartbeatMsg(StormMessage):
    def __init__(self):
        super().__init__(StormAddress.ALL, StormMessageId.HeartbeatMsg)
                
        self.data = [0xFF] #TODO FIXME
        self.pack_string = "c"

# ID 12
class ConfigurationMsg(StormMessage):
    #FIXME idk if that type hint is correct or not...?
    def __init__(self, type: int, param_id: int, value: List[bytes]):
        super().__init__(StormAddress.ALL, StormMessageId.ConfigurationCmd)
                
        self.data = [type, param_id, *value]
        self.pack_string = "BBcccccc" #TODO FIXME how are we doing variable-length configuration stuff????

# ID 13
class ConfigCompleteMsg(StormMessage):
    def __init__(self, num_config_sent: int):
        super().__init__(StormAddress.ALL, StormMessageId.ConfigurationCompleteMsg)
                
        self.data = [num_config_sent]
        self.pack_string = "B"

# ID 20
class RobotVelocityCmd(StormMessage):
    def __init__(self, forward_velocity: float, sideways_velocity: float, rotational_velocity: float):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.RobotVelocityCmd)

        #FIXME multiply/divide by the scaler and all that !!! we can't send straight floats!!!

        self.data = [forward_velocity, sideways_velocity, rotational_velocity]
        self.pack_string = "hhh" # 3 signed int16, I think...? 3 shorts?

# ID 21
class DriveVelocityCmd(StormMessage):
    def __init__(self, front_left_velocity: float, front_right_velocity: float, back_left_velocity: float, back_right_velocity: float):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.DriveVelocitiesCmd)

        #TODO FIXME multiply / divide by the scaler and all that ! we can't send straight floats!

        self.data = [front_left_velocity, front_right_velocity, back_left_velocity, back_right_velocity]
        self.pack_string = "hhhh"


# ID 22
class DriveVoltageCmd(StormMessage):
    def __init__(self, front_left_voltage: float, front_right_voltage: float, back_left_voltage: float, back_right_voltage: float):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.DriveVoltageCmd)
        
        #TODO FIXME multiply / divide by scalers and all that

        self.data = [front_left_voltage, front_right_voltage, back_left_voltage, back_right_voltage]
        self.pack_string = "hhhh"

# ID 23
class DriveRawCmd(StormMessage):
    def __init__(self, front_left_raw: float, front_right_raw: float, back_left_raw: float, back_right_raw: float):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.DriveRawCmd)

        fl_raw = float_to_int16(front_left_raw)
        fr_raw = float_to_int16(front_right_raw)
        bl_raw = float_to_int16(back_left_raw)
        br_raw = float_to_int16(back_right_raw)

        # no scaler for this message, we just go from the min to max range
        self.data = [fl_raw, fr_raw, bl_raw, br_raw]
        self.pack_string = "hhhh"

# ID 24
class DriveFeedbackRsp(StormMessage):
    def __init__(self, forward_velocity: float, sideways_velocity: float, rotational_velocity: float, delta_x: float, delta_y: float, delta_theta: float):
        super().__init__(StormAddress.COMPUTER, StormMessageId.DriveFeedbackRsp)

        #FIXME we need scalers!!!

        self.data = []
        self.pack_string = "hhhhhh"

# ID 25
class BatteryVoltageRsp(StormMessage):
    def __init__(self, voltage: float):
        super().__init__(StormAddress.COMPUTER, StormMessageId.BatteryVoltageRsp)

        #TODO scaler !!!

        self.data = [voltage]
        self.pack_string = "B"

# ID 26
class ClimberHeightCmd(StormMessage):
    def __init__(self, height: float):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.ClimberHeightCmd)

        #TODO scaler

        self.data = [height]
        self.pack_string = "B"

# ID 27
class ClimberVelocityCmd(StormMessage):
    def __init__(self, climber_one_velocity: float, climber_two_velocity: float):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.ClimberVelocityCmd)

        #TODO FIXME need scalers!!!

        self.data = [climber_one_velocity, climber_two_velocity]
        self.pack_string = "hh"

# ID 28
class ClimberRawCmd(StormMessage):
    def __init__(self, climber_one_raw: float, climber_two_raw: float):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.ClimberRawCmd)

        raw_val_one = float_to_int16(climber_one_raw)
        raw_val_two = float_to_int16(climber_two_raw)

        self.data = [raw_val_one, raw_val_two]
        self.pack_string = "hh"

# ID 29
class ClimberPositionCmd(StormMessage):
    def __init__(self, servo_one_position: int, servo_two_position: int):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.ClimberPositionCmd)

        #TODO scalers, units, etc.

        self.data = []
        self.pack_string = "BB"

# ID 30
class ClimberSensorRsp(StormMessage):
    def __init__(self, climber_sensor: bool):
        super().__init__(StormAddress.COMPUTER, StormMessageId.ClimberSensorRsp)

        self.data = [climber_sensor]
        self.pack_string = "?" # 1 bool, I think?

# ID 31
class ClimberStateRsp(StormMessage):
    def __init__(self, climber_one_velocity, climber_two_velocity, climber_height, servo_one_position, servo_two_position, climber_sensor):
        super().__init__(StormAddress.COMPUTER, StormMessageId.ClimberStateRsp)

        #TODO FIXME

        self.data = []
        self.pack_string = "hhBBB?" #FIXME no idea if I did that right

# ID 50
class ShooterVelocityCmd(StormMessage):
    def __init__(self, shooter_velocity: float):
        super().__init__(StormAddress.CANNON, StormMessageId.ShooterVelocityCmd)

        #TODO scaler
        velocity = float_to_uint16(shooter_velocity)

        self.data = [velocity]
        self.pack_string = "H"

# ID 51
class ShooterRawCmd(StormMessage):
    def __init__(self, shooter_raw: float):
        super().__init__(StormAddress.CANNON, StormMessageId.ShooterRawCmd)

        raw_val = float_to_uint16(shooter_raw)

        self.data = [raw_val]
        self.pack_string = "H"

# ID 52
class ShooterPositionCmd(StormMessage):
    def __init__(self, turret_angle: float, hood_angle: float):
        super().__init__(StormAddress.CANNON, StormMessageId.ShooterPositionCmd)

        #TODO FIXME I have no idea what is supposed to go here tbh
        self.data = []
        self.pack_string = "hB"

# ID 53
typedef struct ShooterStateRsp {
    int16_t shooter_velocity;
    int16_t turret_angle;
    uint8_t hood_angle;
} ShooterStateRsp;

// ID 54
typedef struct IndexerVelocityCmd {
    int16_t indexer_velocity;
} IndexerVelocityCmd;

// ID 55
typedef struct IndexerRawCmd {
    int16_t indexer_raw;
} IndexerRawCmd;

// ID 56
typedef struct IndexerFeedCmd {
    uint8_t num_cannonballs;
} IndexerFeedCmd;

// ID 57
typedef struct IntakeVelocityCmd {
    int16_t intake_velocity;
} IntakeVelocityCmd;

// ID 58
typedef struct IntakeFeedCmd {
    uint8_t num_cannonballs;
} IntakeFeedCmd;

// ID 59
typedef struct IntakeRawCmd {
    int16_t intake_raw;
} IntakeRawCmd;

// ID 60
typedef struct IntakeIndexerRsp {
    int16_t intake_velocity;
    int16_t indexer_velocity;
    char ir_sensor_states;
    uint8_t shot_count;
    uint8_t collected_count;
} IntakeIndexerRsp;

// ID 255
typedef struct DebugeMsg {
    char[16] data; //TODO FIXME???
} DebugeMsg;


class DriveVelocitiesCmd(StormMessage):
    def __init__(
        self,
        front_left_velocity: float,
        front_right_velocity: float,
        back_left_velocity: float,
        back_right_velocity: float,
    ):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.DriveVelocitiesCmd)

        # TODO convert using like, the scalers or something

        self.data = [front_left_velocity, front_right_velocity, back_left_velocity, back_right_velocity]
        self.pack_string = "hhhh" # 4 int16's (signed shorts)




if __name__ == "__main__":
    print("RUNNING!")

    test_msg = StormMessage(StormAddress.TRAVERSAL, StormMessageId.DriveVelocitiesCmd)

    print(test_msg)

    print("////////////////////")
