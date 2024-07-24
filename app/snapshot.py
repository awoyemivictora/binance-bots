import asyncio
import websockets
import json
import requests

# WebSocket depth stream URL
uri = "wss://stream.binance.com:9443/ws/bnbbtc@depth"

# Buffer to store events until we get the snapshot
event_buffer = []

# Local order book structure
local_order_book = {
    'bids': {},
    "asks": {}
}

async def depth_event_handler(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            event = await websocket.recv()
            event_buffer.append(json.loads(event))
            

async def fetch_depth_snapshot():
    snapshot_url = "https://api.binance.com/api/v3/depth?symbol=BNBBTC&limit=1000"
    snapshot = requests.get(snapshot_url).json()
    return snapshot


def initialize_local_order_book(snapshot):
    global last_update_id
    last_update_id = snapshot['lastUpdateId']
    local_order_book['bids'] = {float(price): float(quantity) for price, quantity in snapshot['bids']}
    local_order_book['asks'] = {float(price): float(quantity) for price, quantity in snapshot['asks']}
    

def process_event(event):
    for price, quantity in event['b']:
        price = float(price)
        quantity = float(quantity)
        if quantity == 0:
            if price in local_order_book['bids']:
                del local_order_book['bids'][price]
        else:
            local_order_book['bids'][price] = quantity
            
    
    for price, quantity in event['a']:
        price = float(price)
        quantity = float(quantity)
        if quantity == 0:
            if price in local_order_book['asks']:
                del local_order_book['asks'][price]
        
        else:
            local_order_book['asks'][price] = quantity
            

async def main():
    # Start buffering events
    asyncio.create_task(depth_event_handler(uri))
    
    # Get the dept snapshot
    snapshot = await fetch_depth_snapshot()
    initialize_local_order_book(snapshot)
    
    # Process buffered events
    global last_update_id
    while event_buffer:
        event = event_buffer.pop(0)
        if event['u'] <= last_update_id:
            continue
        if event['U'] <= last_update_id + 1 and event['u'] >= last_update_id + 1:
            process_event(event)
            last_update_id =    event['u']
            break
        
    # Continuosly process new events
    while True:
        if event_buffer:
            event = event.buffer.pop(0)
            if event['U'] == last_update_id + 1:
                process_event(event)
                last_update_id = event['u']
            elif event['U'] > last_update_id + 1:
                # If we missed any events, reinitialize from snapshot
                snapshot = await fetch_depth_snapshot()
                initialize_local_order_book(snapshot)
                event_buffer()
                

# Run the main function
asyncio.run(main())