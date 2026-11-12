import asyncio
import json
import random
import websockets

async def send_data(websocket):
    try:
        while True:
            
            data = {
                "bandwidth": round(random.uniform(0, 500), 2),
                "status": "Online"
            }
            
            
            await websocket.send(json.dumps(data))
            await asyncio.sleep(2)
    except websockets.exceptions.ConnectionClosed:
        print("Websocket Server Disconnected")

async def main():
   
    async with websockets.serve(send_data, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())