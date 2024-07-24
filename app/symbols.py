import os
from dotenv import load_dotenv
from binance.spot import Spot as Client
from binance.error import ClientError

# Load environment variables
load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")

# Define proxy settings
proxies = {'https': 'http://1.2.3.4:8080'}

# Initialize the client with proxy settings and API keys
client = Client(api_key, api_secret, base_url = 'https://api1.binance.com')

# Define the symbols you are interested in
symbols_to_check = ["BNBUSDT", "BTCUSDT"]

def fetch_exchange_info(client, symbols_to_check, retries=5, delay=3):
    for attempt in range(retries):
        try:
            # Fetch exchange information for all symobls
            exchange_info = client.exchange_info()

            # Extract and display information for the specified symbols
            for symbol_info in exchange_info['symbols']:
                if symbol_info['symbol'] in symbols_to_check:
                    symbol = symbol_info['symbol']
                    status = symbol_info['status']
                    base_asset = symbol_info['baseAsset']
                    quote_asset = symbol_info['quoteAsset']
                    permissions = symbol_info.get['permissions', []]

                    print(f"Symbol: {symbol}")
                    print(f"  Status: {status}")
                    print(f"  Base Asset: {base_asset}")
                    print(f"  Quote Asset: {quote_asset}")
                    print(f"  Permissions: {permissions}")
                    print() # Newline for better readability
            return


        except ClientError as e:
            print(f"An error occured: {e.error_code} - {e.error_message}")
            break
        except Exception as e:
            print(f"Attemp {attempt + 1} failed with error: {e}")
            break
            time.sleep(delay)


# Attempt to fetch exchange info with retry logic
fetch_exchange_info(client, symbols_to_check)













