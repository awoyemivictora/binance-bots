import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    print(f"Price: {data['p']}")


def on_error(ws, error):
    print(error)
    

def on_close(ws):
    print("Connection closed")
    
    
def on_open(ws):
    print("Connection opened")
    

if __name__ == "__main__":
    # socket = "wss://stream.binance.com:9443/ws/btcusdt@trade"
    socket = "wss://stream.binance.com:9443/ws/btcusdt@aggTrade"
    ws = websocket.WebSocketApp(
            socket,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    
    
    
    