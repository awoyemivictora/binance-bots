import asyncio
import websockets

async def listen():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                print(f"Received: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            
async def pong_handler(websocket):
    while True:
        try:
            pong = await websocket.ping()
            await pong
            print("Pong sent in response to ping")
        except websockets.exceptions.ConnectionClosed:
            print("Connection closed")
            break
        
async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        pong_task = asyncio.ensure_future(pong_handler(websocket))
        try:
            await listen()
        finally:
            pong_task.cancel()
            

asyncio.get_event_loop().run_until_complete(main())