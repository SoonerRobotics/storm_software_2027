import struct

try:
    import serial
except ImportError:
    serial = None

class Electrical_Interface():
    def __init__(self, port=None, baudrate=115200):
        self.ser = None
        # define our vars
        self.vars = {
            'forward': 0.0,
            'turn': 0.0,
            'cannon_x': 0.0,
            'cannon_y': 0.0,
        }
        self.msg = None
        # we can't do anything without pyserial
        if port is not None:
            if serial is None:
                raise RuntimeError("pyserial is required to open an electrical serial connection")
            self.ser = serial.Serial(port, baudrate)
    
    def update_vars(self, updates: dict):
        for name, value in updates.items():
            if name not in self.vars:
                raise KeyError(f"Unknown electrical variable: {name}")
            self.vars[name] = value
    
    def pack_msg(self):
        # this updates our variables into the message
        self.msg = struct.pack(
            '<ffff',
            self.vars['forward'],
            self.vars['turn'],
            self.vars['cannon_x'],
            self.vars['cannon_y'],
        )
    
    def send_msg(self):
        self.pack_msg()
        # send our message to the serial interface
        if self.ser is not None:
            self.ser.write(self.msg)

    def send_command(self, command: str, payload=None):
        # TODO this is for like oneshot commands like firing the cannon, but this needs to be fixed
        raise NotImplementedError(
            "Board protocol is not defined yet, pending Arduino interface or if we just write it straight through serial"
        )