import requests

try:
    response = requests.get("https://api.binance.com/api/v3/ping")
    if response.status_code == 200:
        print("Network connectivity to Binance API is successful.")
    else:
        print(f"Failed to connect to Binance API. Status code: {response.status_code}")
except Exception as e:
    print(f"An error occurred: {e}")
