import json
import os
from dotenv import load_dotenv
from binance.spot import Spot as Client
from binance.websocket.spot.websocket_api import SpotWebsocketStreamClient as WebsocketClient

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")

# Initialize Binance Spot client
client = Client(api_key, secret_key, base_url='https://testnet.binance.vision')

# def main():
    # Get server timestamp
    # print(client.time())

    # Get klines of BTCUSDT at 1m interval
    # klines = client.klines("BTCUSDT", "1m")
    # print(json.dumps(klines, indent=2))

    # Get last 10 klines of BNBUSDT at 1h interval
    # klines_10 = client.klines("BNBUSDT", "1h", limit=10)
    # print(json.dumps(klines_10, indent=2))
    
    # Get account and balance information
    # account_info = client.account()
    # print(json.dumps(account_info, indent=2))
    
    # Post a new order
    # params = {
    #     'symbol': 'BTCUSDT',
    #     'side': 'SELL',
    #     'type': 'MARKET',
    #     'quantity': 0.002,
    # }
    # response = client.new_order(**params)
    # print(json.dumps(response, indent=2))

    # Get order
    # get_order = client.get_order('BTCUSDT', orderId=6480651)
    # print(json.dumps(get_order, indent=2))
    

def message_handler(message):
    print(message)

ws_client = WebsocketClient()
ws_client.start()

ws_client.mini_ticker(
    symbol='bnbusdt',
    id=1,
    callback=message_handler,
)

# Combine selected streams
ws_client.instant_subscribe(
    stream=['bnbusdt@bookTicker', 'ethusdt@bookTicker'],
    callback=message_handler,
)

ws_client.stop()
    
    
if __name__ == "__main__":
    message_handler()
