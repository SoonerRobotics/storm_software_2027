# TODO standard file header
# TODO also talk about STORMLib and where it is defined

from enum import Enum, unique
from struct import pack

# TODO docstring
@unique
class StormAddress(Enum):
    ALL = 0
    COMPUTER = 1
    TRAVERSAL = 2
    CANNON = 3


# TODO docstring
# also TODO this is old
@unique
class StormMessageId(Enum):
    ComputerRequest = 10
    Heartbeat = 11
    Configuration = 12
    ConfigComplete = 13
    RobotVelocity = 20
    DriveVelocity = 21
    DriveVoltage = 22
    DriveRaw = 23
    DriveFeedback = 24
    BatteryVoltage = 25
    TaskCommand = 30
    TaskResponse = 31
    NONE = 255  # this is special and used for testing only


# TODO docstring
class StormMessage:
    START_BYTE = 0xAA
    END_BYTE = 0xFF

    def __init__(self, address: StormAddress, id: StormMessageId):
        # TODO docstring
        self.address = address
        self.id = id

        self.data = bytearray()  # this will be set by subclasses
        self.pack_string = (
            ""  # defines how self.data is supposed to get struct.pack()ed
        )

    def __repr__(self) -> str:
        #TODO docstring
        #TODO maybe this could be better
        return f"{self.START_BYTE} {self.address} {self.id} size??? {self.data} {self.END_BYTE}"

    def pack(self) -> bytes:
        # TODO docstring
        # override me ?? not necessarily. subclasses just need to define HOW self.data gets packed?

        packed_msg = struct.pack()

        # TODO: pack the data first, and then

        size = len(self.data)
        # TODO: pack the rest of the message
        return


# what data does each message have?
# it has how to encode itself, obviously
# but also we want named fields for everything... so uh...


class DriveVelocityCmd(StormMessage):
    def __init__(
        self,
        front_left_velocity: float,
        front_right_velocity: float,
        back_left_velocity: float,
        back_right_velocity: float,
    ):
        super().__init__(StormAddress.TRAVERSAL, StormMessageId.DriveVelocity)

        # TODO convert using like, the scalers or something

        self.data = bytearray(
            front_left_velocity,
            front_right_velocity,
            back_left_velocity,
            back_right_velocity,
        )




if __name__ == "__main__":
    print("RUNNING!")

    test_msg = StormMessage(StormAddress.TRAVERSAL, StormMessageId.DriveVelocity)

    print(test_msg)

    print("////////////////////")
