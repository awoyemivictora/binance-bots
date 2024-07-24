#!/usr/bin/env python

import os
from dotenv import load_dotenv
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError
import json

load_dotenv()

config_logging(logging, logging.DEBUG)
logger = logging.getLogger(__name__)

api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")


client = Client(api_key, api_secret, base_url='https://testnet.binance.vision')

   
try:
    response = client.cancel_open_orders("BTCUSDT")
    logging.info(response)
    print(json.dumps(response, indent=4))
except ClientError as error:
    error_msg = {
        "status": error.status_code,
        "error_code": error.error_code,
        "error_message": error.error_message
    }
    logging.error(error_msg)
    print(json.dumps(error_msg, indent=4))