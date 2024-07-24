import os
from dotenv import load_dotenv
from binance.spot import Spot as Client

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")

proxies = { 'https': 'http://1.2.3.4:8080'}

client = Client(api_key, api_secret, base_url='https://api1.binance.com', proxies=proxies)

# print(client.accept_quote(10))
a = client.exchange_info(symbol="BNBUSDT", permissions="SPOT")
print(a)

