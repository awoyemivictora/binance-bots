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
    response = client.one_time_transaction("MAIN_SITE", 10.1, "USDT", recvWindow=5000)
    logger.info(response)
except ClientError as error:
    logger.error("Found error. status: {}, error code: {}, error message: {}".format(
        error.status_code, error.error_code, error.error_message
    ))
    
    
    