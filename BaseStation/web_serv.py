import asyncio
from websocket_server import WebsocketServer
import time
from json import loads, dumps

class Serve():
    def __init__(self):
        self.server = WebsocketServer(host='192.168.1.128', port=8765)
        self.server.set_fn_new_client(self.new_client)
        self.server.set_fn_client_left(self.client_left)
        self.server.set_fn_message_received(self.on_message)
        self.connections = {}
    
    def new_client(self, client, server):
        print("new client")

    def client_left(self, client, server):
        print("client left")
    
    def on_message(self, client, server, message):
        #print(message)
        msg = loads(message)
        if(msg["Header"] == "Init"):
            self.connections[msg["Sender"]] = client
            print(msg["Message"])
            
        else:
            try:
                self.server.send_message(client=self.connections[msg["Recipient"]], msg=message)  
            except:
                print("Recipient Currently Unavailable")
  
    def run(self):
        print('started')
        self.server.run_forever()
    
if __name__ == "__main__":
    server = Serve()
    server.run()