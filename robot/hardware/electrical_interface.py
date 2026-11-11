#TODO: standard file header or something

import serial



#TODO: document
class ElectricalInterface():
    def __init__(self):
        self.serial = serial.Serial() #TODO: specify what options we want
        # also TODO there is Serial.rs485_mode

        pass

    def open(self) -> bool:
        successful = False

        try:
            #TODO: check if we are already open?
            self.serial.open()
            successful = True

        except Exception as e:
            #TODO ???
            successful = False

        return successful #TODO: log this somewhere or something? continually retry to open?


    def close(self) -> bool:
        self.serial.close() #TODO FIXME?
        pass


    def run(self) -> bool:
        #TODO ?????
        pass

#TODO: thread worker or something

#TODO: ???? wait why did I write that?

