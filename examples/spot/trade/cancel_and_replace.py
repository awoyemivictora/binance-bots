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

try:
    response = client.cancel_and_replace(
        "BNBUSDT",
        "SELL",
        "LIMIT",
        "STOP_ON_FAILURE",
        timeInForce="GTC",
        quantity=10.1,
        price=295.92,
        # The order with this id (cancelOrderId) has to be able to be cancelled.
        # If you wish to test, create an open order first, then copy and paste id
        cancelOrderId=1013156,
        recvWindow=5000,
    )
    logging.info(response)
except ClientError as error:
    logging.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )




