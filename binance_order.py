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

# Function to get the Binance server time
def get_server_time():
    try:
        server_time = client.time()
        return server_time['serverTime']
    except ClientError as error:
        logger.error("Failed to get server time: {}".format(error))
        return None

# Function to synchronize local time with Binance server time
def synchronize_time():
    server_time = get_server_time()
    if server_time:
        local_time = int(time.time() * 1000)
        time_diff = server_time - local_time
        logger.info("Time difference: {} ms".format(time_diff))
        return time_diff
    else:
        return 0
    
# Synchronize time
time_diff = synchronize_time()

def place_order():
    symbol = symbol_entry.get()
    side = side_var.get()
    order_type = order_type_var.get()
    quantity = quantity_entry.get()
    price = price_entry.get()
    
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": float(quantity),
        "timestamp": int(time.time() * 1000) + time_diff # Adjust the timestamp
    }
    
    if order_type == "LIMIT":
        params["price"] = float(price)
        params["timeInForce"] = "GTC"

    try:
        response = client.new_order(**params)
        logging.info(response)
        pretty_response = json.dumps(response, indent=4)
        messagebox.showinfo("Order Response", pretty_response)
    except ClientError as error:
        error_msg = {
            "status": error.status_code,
            "error_code": error.error_code,
            "error_message": error.error_message
        }
        logging.error(error_msg)
        pretty_error_msg = json.dumps(error_msg, indent=4)
        messagebox.showerror("Order Error", pretty_error_msg)
        

# Create the main window
root = tk.Tk()
root.title("Binance Order GUI")
root.geometry("500x500")

# Create and place the labels and entries
tk.Label(root, text="Symbol:").grid(row=0, column=0)
symbol_entry = tk.Entry(root)
symbol_entry.grid(row=0, column=1, pady=20)

tk.Label(root, text="Side:").grid(row=1, column=0)
side_var = tk.StringVar(value="BUY")
tk.OptionMenu(root, side_var, "BUY", "SELL").grid(row=1, column=1)

tk.Label(root, text="Order Type:").grid(row=2, column=0)
order_type_var = tk.StringVar(value="LIMIT")
tk.OptionMenu(root, order_type_var, "LIMIT", "MARKET").grid(row=2, column=1)

tk.Label(root, text="Quantity:").grid(row=3, column=0)
quantity_entry = tk.Entry(root)
quantity_entry.grid(row=3, column=1)

tk.Label(root, text="Price (for LIMIT orders):").grid(row=1, column=0)
price_entry = tk.Entry(root)
price_entry.grid(row=4, column=1)


# Create and place the order button
order_button = tk.Button(root, text="Place Order", command=place_order)
order_button.grid(row=5, columnspan=2)


# Run the main event loop
root.mainloop()
        
        
        