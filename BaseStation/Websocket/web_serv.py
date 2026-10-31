import asyncio
from websockets.asyncio.server import serve

async def msg(websocket):
    try:
        async for message in websocket:
            print(f"Received {type(message).__name__}: {message}")
    except Exception as exc:
        print(f"Server handler error: {exc!r}")
        raise

async def main():
    server = await serve(msg, "192.168.1.128", 8765, ping_interval=None)
    print("Server started")
    await server.serve_forever()

asyncio.run(main())