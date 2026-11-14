#TODO: standard file header or something

import serial
import struct


#TODO: document
class ElectricalInterface():
    def __init__(self):
        self.serial = serial.Serial() #TODO: specify what options we want
        # also TODO there is Serial.rs485_mode

        #not sure how we want to store info yet, maybe dict then iterate through that when packing?
        self.vars = {'yada': 'yada',
                        'more': 'yada'}
        self.msg = None
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
    
    def update_vars(self, updates: dict):
        #for other stuff to call to put their info into the msg  
        for x in updates:
            self.vars[x] = updates[x]
    
    def pack_msg(self):
        #put all the stuff we need to update into a struct msg to send
        tmp = []
        for val in self.vars:
            tmp.append(self.vars[val])
        self.msg = struct.pack(tmp)
        pass
    
    def send_msg(self):
        #send the stuff to electrical
        self.pack_msg()
        self.serial.write(self.msg)

#TODO: thread worker or something

#TODO: ???? wait why did I write that?

