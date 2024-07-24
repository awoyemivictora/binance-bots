# Server Code
import asyncio
import websockets
import time

async def ping_pong_handler(websocket, path):
    try:
        while True:
            await asyncio.sleep(60) # 3 minutes
            ping_payload = str(time.time()).encode('utf-8')
            await websocket.ping(ping_payload)
            print("Ping sent")
    except websockets.exceptions.ConnectionClosed:
        print("Connection closed")
        
        
async def handler(websocket, path):
    ping_task = asyncio.ensure_future(ping_pong_handler(websocket, path))
    try:
        async for message in websocket:
            print(f"Received message: {message}")
    finally:
        ping_task.cancel()
        

start_server = websockets.serve(handler, 'localhost', 8765)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
