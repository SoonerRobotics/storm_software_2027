import asyncio
import websockets
import json
import signal

CLIENTS = set()

async def handler(websocket):
    CLIENTS.add(websocket)
    try:
        async for message in websocket:
            await websocket.send(f"echo: {message}")
            others = CLIENTS - {websocket}
            data = json.dumps({"from": id(websocket), "msg": message})
            websockets.broadcast(others, data)
    except websockets.ConnectionClosed:
        pass
    finally:
        CLIENTS.discard(websocket)

async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(handler, "192.168.1.98", 8765):
        print("Server running on ws://192.168.1.98:8765")
        await stop  # Run until SIGTERM

if __name__ == "__main__":
    asyncio.run(main())