import asyncio
import websockets
import random

async def connect_with_backoff(uri):
    delay = 1
    while True:
        try:
            async with websockets.connect(uri) as ws:
                delay = 1  # Reset on success
                async for message in ws:
                    print(f"Received: {message}")
        except (websockets.ConnectionClosed, OSError) as e:
            jitter = random.uniform(0, delay * 0.5)
            wait = min(delay + jitter, 30)
            print(f"Disconnected ({e}), retry in {wait:.1f}s")
            await asyncio.sleep(wait)
            delay = min(delay * 2, 30)

asyncio.run(connect_with_backoff("ws://0.0.0.0:8765"))