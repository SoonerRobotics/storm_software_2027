from Camera.driver_camera import Camera
import asyncio
import websocket
from json import dumps

class Robot():
    def __init__(self, shm, buf):
        self.shm = shm
        self.cam = Camera(self.shm, buf)
        self.connected = False
        self.ws = websocket.WebSocket()
        self.msg = {"Header": "Init",
                    "Sender": "Robot",
                    "Recipient": None,
                    "Message": "Hello Server from Robot"}
        
    
    def start(self):
        self.ws.connect("ws://192.168.1.128:8765")
        init_msg = dumps(self.msg)
        self.ws.send(init_msg)
        self.connected = True
    
    def close(self):
        self.cam.close()
    
    def send_camera(self):
        self.cam.send_frame()

    
    def send_bw(self):
        self.msg = {"Header": "Msg",
                    "Sender": "Robot",
                    "Recipient": "Base Station",
                    "Message": f"{self.cam.bw}"}
        self.ws.send(dumps(self.msg))
        
    def on_message(ws, message):
        print(message)