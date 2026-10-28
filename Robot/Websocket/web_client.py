
from websockets.sync.client import connect
import asyncio

async def send_bandwith():
    with connect("ws://192.168.1.128:8765") as websocket:
        while True:
            uIn = input("Message: ")
            websocket.send(uIn)
            #message = websocket.recv()
            #print(f"Received: {message}")


asyncio.run(send_bandwith())