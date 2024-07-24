#!/usr/bin/env python

import os
from dotenv import load_dotenv
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError
import json
import tkinter as tk
from tkinter import messagebox
import time
import requests

# Load environment variables
load_dotenv()

# Configure logging
config_logging(logging, logging.DEBUG)
logger = logging.getLogger(__name__)

# Get API keys from environment variables
api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")


# Initialize the Binance client
client = Client(api_key, api_secret, base_url='https://testnet.binance.vision')


# params = {
#     "symbol": "BNBUSDT",
#     "side": "SELL",
#     "quantity": 0.002,
#     "price": "510",
#     "stopPrice": "500",
#     "stopLimitPrice": "495",
#     "stopLimitTimeInForce": "GTC"
# }

# try:
#     response = client.new_oco_order(
#         symbol=params["symbol"],
#         side=params["side"],
#         quantity=params["quantity"],
#         price=params["price"],
#         stopPrice=params["stopPrice"],
#         stopLimitPrice=params["stopLimitPrice"],
#         stopLimitTimeInForce=params["stopLimitTimeInForce"],
#         aboveType="LIMIT_MAKER",
#         belowType="STOP_LOSS_LIMIT"
#     )
#     logging.info(response)
#     print(json.dumps(response, indent=4))
# except ClientError as error:
#     error_msg = {
#         "status": error.status_code,
#         "error_code": error.error_code,
#         "error_message": error.error_message
#     }
#     logging.error(error_msg)
#     print(json.dumps(error_msg, indent=4))
    

# # GUI Part (If you want to integrate with Tkinter)
# def place_order():
#     symbol = symbol_entry.get()
#     side = side_entry.get()
#     quantity = float(quantity_entry.get())
#     price = price_entry.get()
#     stopPrice =stop_price_entry.get()
#     stopLimitPrice = stop_limit_price_entry.get()
#     stopLimitTimeInForce = "GTC" # Can be a fixed value or user input
    
#     try:
#         response = client.new_oco_order(
#             symbol=symbol,
#             side=side,
#             quantity=quantity,
#             price=price,
#             stopPrice=stopPrice,
#             stopLimitPrice=stopLimitPrice,
#             stopLimitTimeInForce=stopLimitTimeInForce,
#             # aboveType="LIMIT_MAKER",
#             # belowType="STOP_LOSS_LIMIT"
#         )
#         logging.info(response)
#         messagebox.showinfo("Order Response", json.dumps(response, indent=4))
#     except ClientError as error:
#         error_msg = {
#             "status": error.status_code,
#             "error_code": error.error_code,
#             "error_message": error.error_message
#         }
#         logging.error(error_msg)
#         messagebox.showerror("Order Error", json.dumps(error_msg, indent=4))
        

# # Tkinter setup
# root = tk.Tk()
# root.title("Binance OCO Order")
# root.geometry("500x500")

# tk.Label(root, text="Symbol").grid(row=0)
# tk.Label(root, text="Side").grid(row=1)
# tk.Label(root, text="Quantity").grid(row=2)
# tk.Label(root, text="Price").grid(row=3)
# tk.Label(root, text="Stop Price").grid(row=4)
# tk.Label(root, text="Stop Limit Price").grid(row=5)

# symbol_entry = tk.Entry(root)
# side_entry = tk.Entry(root)
# quantity_entry = tk.Entry(root)
# price_entry = tk.Entry(root)
# stop_price_entry = tk.Entry(root)
# stop_limit_price_entry = tk.Entry(root)
    
# symbol_entry.grid(row=0, column=1)
# side_entry.grid(row=1, column=1)
# quantity_entry.grid(row=2, column=1)
# price_entry.grid(row=3, column=1)
# stop_price_entry.grid(row=4, column=1)
# stop_limit_price_entry.grid(row=5, column=1)

# tk.Button(root, text="Place Order", command=place_order).grid(row=6, column=0, columnspan=2)

# root.mainloop()
    
    
    
    
    
    
    
params = {
    "symbol": "BNBUSDT",
    "side": "SELL",
    "quantity": 0.002,
    "aboveType": "LIMIT_MAKER",
    "belowType": "LIMIT_MAKER",
    "abovePrice": 510,
    "belowPrice": 500,
}

client = Client(api_key, api_secret, base_url="https://testnet.binance.vision")

try:
    response = client.new_oco_order(**params)
    logging.info(response)
except ClientError as error:
    logging.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )
    
    
    
    