#TODO docstring, standard file header, etc.


from serial import Serial

from robot.electronics.storm_message import StormAddress, StormMessage, StormMessageId

START_BYTE = 0xAA
END_BYTE = 0x55
BAUD_RATE = 115200

MAX_DATA_SIZE = 12
MIN_DATA_SIZE = 1
MAX_MSG_SIZE = 16
MIN_MSG_SIZE = 6


class StormBus:
    def __init__(self, address: StormAddress, srl: Serial, useRS485: bool = True):
        self.address = address

        self.srl = srl
        self.useRS485 = useRS485

        # === protocol definitions ===
        self.tempAddr = StormAddress.ALL
        self.tempSize = 255
        self.tempType = StormMessageId.DebugeMsg
        self.tempData = []
        # ============================

        # pins
        # int txPin = 0
        # int rxPin = 0
        # int txEnablePin = 0
        # int rxEnablePin = 0

        self.isTransmitting = False
        

    def close(self) -> None:
       #TODO do we even need this here???
       self.srl.close() #????

    #TODO FIXME do we even need this? do we have the hardware pins for it???
    def init(self) -> bool:
        self.srl.begin(BAUD_RATE)

        if self.address == StormAddress.COMPUTER:
            # enable receiving messages
            #digitalWrite(self.rxEnablePin, LOW)
            pass
        
        # indicate that we connecteds
        # digitalWrite(self.BUILTIN_LED_PIN, HIGH)

        return True

    #TODO: rename this to uint8_t GetMessage() and have it return the address
    # or alternatively name it like PollForMessage() or TryReceiveMessage() or something
    def has_message(self) -> bool:
        # Address tempAddress
        # Message tempType
        # uint8_t tempSize
        # char tempDATA[16]

        if self.isTransmitting:
            return False
        
        #TODO: do we need to enable receive pin here?

        # minimum message size, according to spec, is 6 bytes
        if self.srl.in_waiting < MIN_MSG_SIZE:
            return False
        
        # check for start byte (0xAA)
        foundMsg = False
        while self.srl.peek() != -1:
            if self.srl.read() == START_BYTE:
                foundMsg = True
                break

        if not foundMsg:
            return False

        #FIXME: I don't think we need all these peek() calls, like, we already checked serial.available()

        # next byte is address
        if self.srl.peek() != -1:
            tempAddress = StormAddress(self.srl.read())

            # handle broadcast messages (like heartbeat)
            if tempAddress == StormAddress.ALL:
                #TODO handle heartbeat

                return False # ???
            elif tempAddress != self.address:
                return False

        # next byte is type
        if self.srl.peek() != -1:
            tempType = StormMessageId(self.srl.read())

        # next byte is size
        if self.srl.peek() != -1:
            tempSize = int(self.srl.read())

            # maximum message size is 16 according to the spec
            if tempSize < 0 or tempSize > MAX_MSG_SIZE:
                return False


        # next SIZE bytes are data
        for i in range(tempSize):
            tempDATA[i] = self.srl.read()

        # read stop byte
        if self.srl.peek() != -1:
            if self.srl.read() != END_BYTE:
                return False

        #FIXME this will conflict with like, the address variable we should do something
        self.address = tempAddress
        self.size = tempSize
        self.type = tempType

        # transfer DATA too
        for i in range(tempSize):
            DATA[i] = tempDATA[i]


        return True

    def get_message(self) -> StormMessage:
        """Get a StormMessage object.
        Once you've identified that there's a message for you (via HasMessage()),
        use this to get the message object.
        then check the message's type/ID to see which one it is,
        then use the various msg.AsMessgeType() functions to get a struct.
        alternatively you can work with the raw DATA[] array, if you know what you're doing."""
        
        # create the message object from the stored information
        msg = StormMessage(self.type, self.address, self.size, self.DATA)

        return msg

    #TODO FIXME we don't actually need this right?
    def send_response(self, msg: StormMessage) -> bool:
        """Send a response back to the robot's computer.
        Use this function to SEND messages FROM your board."""
        
        # # start transmission
        # self.isTransmitting = True
        # digitalWrite(self.txEnablePin, HIGH)
        # delayMicroseconds(50)

        # # write start byte
        # self.srl.write(self.START_BYTE)

        # # write address (always computer for a response)
        # self.srl.write(msg.address)

        # # write message ID
        # self.srl.write(msg.type)

        # # write size
        # self.srl.write(msg.size)

        # # finally write the data
        # for (int i = 0 i < msg.size i++:
        #     self.srl.write(msg.DATA[i])
        # }

        # # write end byte
        # self.srl.write(self.END_BYTE)

        # # wait for entire buffer to send
        # self.srl.flush()

        # delayMicroseconds(50)
        # digitalWrite(self.txEnablePin, LOW)
        # self.isTransmitting = False

        # return True # return True on success

