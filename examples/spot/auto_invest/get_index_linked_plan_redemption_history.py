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

proxies = { 'https': 'http://1.2.3.4:8080'}

client = Client(api_key, api_secret, base_url='https://api1.binance.com', proxies=proxies)

try:
    response = client.get_index_linked_plan_redemption_history(12345, recvWindow=5000)
    logger.info(response)
except ClientError as error:
    logger.error(
        "Found error. status: {}, error code: {}, error message: {}".format(
            error.status_code, error.error_code, error.error_message
        )
    )