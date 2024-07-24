#!/usr/bin/env python

import os
from dotenv import load_dotenv
import logging
import pandas as pd
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError

load_dotenv()

config_logging(logging, logging.DEBUG)
logger = logging.getLogger(__name__)

api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")

params = {
    "symbol": "BTCUSDT",
    "side": "SELL",
    "type": "MARKET",
    # "timeInForce": "GTC",
    "quantity": 0.002,
    # "price": 9500,
}

client = Client(api_key, api_secret, base_url='https://testnet.binance.vision')

# def print_exchange_info():
#     try:
#         exchange_info = client.exchange_info()
#         print("Exchange Info:")
#         print(pd.json_normalize(exchange_info))
#         logger.info("Exchange info printed")
#     except Exception as e:
#         logger.error("Error fetching exchange info: {}".format(e))
#         print("Error fetching exchange info: {}".format(e))

# def get_minimum_notional(symbol):
#     try:
#         exchange_info = client.exchange_info()
#         for s in exchange_info['symbols']:
#             if s['symbol'] == symbol:
#                 for f in s['filters']:
#                     if f['filterType'] == 'MIN_NOTIONAL':
#                         return float(f['minNotional'])
#         logger.error("MIN_NOTIONAL filter not found for symbol {}".format(symbol))
#         print("MIN_NOTIONAL filter not found for symbol {}".format(symbol))
#         return None
#     except Exception as e:
#         logger.error("Error fetching exchange info: {}".format(e))
#         print("Error fetching exchange info: {}".format(e))
#         return None

# try:
#     print_exchange_info() # Print exchange info for debugging
    
#     # Define the trading pair and order details
#     symbol = "ETHUSDT"
#     quantity = 0.001
    
#     # Fetch minimum notional value
#     min_notional = get_minimum_notional(symbol)
#     if min_notional is None:
#         logger.error("Minimum notional value not found for symbol {}".format(symbol))
#         print("Minimum notional value not found for symbol {}".format(symbol))
#     else:
#         # Fetch current price to calculate notional value
#         ticker_price = client.ticker_price(symbol)
#         current_price = float(ticker_price['price'])
#         notional_value = quantity * current_price
        
#         if notional_value >= min_notional:
#             # Fetch account information
#             response = client.account(recvWindow=5000)
#             balances = response['balances']
            
#             # Display account information using pandas DataFrame
#             df_balances = pd.DataFrame(balances)
#             df_balances['free'] = df_balances['free'].astype(float)
#             df_balances['locked'] = df_balances['locked'].astype(float)
#             df_balances = df_balances[(df_balances['free'] > 0) | (df_balances['locked'] > 0)]
#             print("Account Balances:")
#             print(df_balances)
            
#             # Place a test order
#             test_order = client.new_order(
#                 symbol=symbol,
#                 side="BUY",
#                 type="MARKET",
#                 quantity=quantity,
#                 recvWindow=5000
#             )
#             logger.info(test_order)
#             print("Test Order: ")
#             df_order = pd.DataFrame([test_order])
#             print(df_order)
            
#             # Fetch account information again to see the updated balances
#             updated_response = client.account(recvWindow=5000)
#             updated_balances = updated_response['balances']
            
#             # Display updated account information using pandas DataFrame
#             df_updated_balances = pd.DataFrame(updated_balances)
#             df_updated_balances['free'] = df_updated_balances['free'].astype(float)
#             df_updated_balances['locked'] = df_updated_balances['locked'].astype(float)
#             df_updated_balances = df_updated_balances[(df_updated_balances['free'] > 0) | (df_updated_balances['locked'] > 0)]
#             print("Updated Account Balances:")
#             print(df_updated_balances)
#         else:
#             logger.error("Order not placed. Notional value {} is below the minimum required {}".format(notional_value, min_notional))
#             print("Order not placed. Notional value {} is below the minimum required {}".format(notional_value, min_notional))
    
# except ClientError as error:
#     logger.error(
#         "Found error. status: {}, error code: {}, error message: {}".format(
#             error.status_code, error.error_code, error.error_message
#         )
#     )
    
#     print(f"Error: {error.status_code}, {error.error_code}, {error.error_message}")
    
 