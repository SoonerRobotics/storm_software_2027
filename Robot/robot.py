from Camera.driver_camera import Camera
import asyncio
import websocket

class Robot():
    def __init__(self, shm, buf):
        self.shm = shm
        self.cam = Camera(self.shm, buf)
        self.connected = False
        self.ws = websocket.WebSocket()
        
    
    def start(self):
        self.ws.connect("ws://192.168.1.128:8765")
        self.connected = True
    
    def close(self):
        self.cam.close()
    
    def send_camera(self):
        self.cam.send_frame()

    
    def send_bw(self):
        self.ws.send(self.cam.bw)
        
    def on_message(ws, message):
        print(message)