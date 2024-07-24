#!/usr/bin/env python

import os
from dotenv import load_dotenv
import logging
from binance.spot import Spot as Client
from binance.lib.utils import config_logging
from binance.error import ClientError

load_dotenv()

config_logging(logging, logging.DEBUG)
logger = logging.getLogger(__name__)

api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")

proxies = None

client = Client(api_key, api_secret, base_url='https://testnet.binance.vision', proxies=proxies)

# try:
#     response = client.get_target_asset_list(
#         targetAsset="BTC", size=100, current=1, recvWindow=5000
#     )
#     logger.info(response)
# except ClientError as error:
#     logger.error(
#         "Found error. status: {}, error code: {}, error message: {}".format(
#             error.status_code, error.error_code, error.error_message
#         )
#     )

try:
    response = client.account(recvWindow=5000)
    logger.info(response)
    print(response)

    
    test_order = client.new_order(
        symbol="ETHUSDT",
        side="BUY",
        type="MARKET",
        quantity=0.01,
        recvWindow=5000
    )
    logger.info(test_order)
    print(test_order)
except ClientError as error:
    logger.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )
    
    print(f"Error: {error.status_code}, {error.error_code}, {error.error_message}")
    
    