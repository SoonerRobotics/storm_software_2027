import struct, serial

class Electrical_Interface():
    def __init__(self):
        #create the serial sever adn stuff
        self.ser = serial.Serial('blah blah fix later')
        #not sure how we want to store info yet, maybe dict then iterate through that when packing?
        self.vars = {'yada': 'yada',
                     'more': 'yada'}
        self.msg = None
        pass
    
    def update_vars(self, updates: dict):
        
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
        self.ser.write(self.msg)
        