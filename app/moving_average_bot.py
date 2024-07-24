import os
import time
from dotenv import load_dotenv
from binance.client import Client
import pandas as pd
import logging


# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("SECRET_KEY")

# Initialize Binance client for testnet
client = Client(api_key, api_secret, testnet=True)

# Set up logging
logging.basicConfig(level=logging.INFO, filename='bot.log', format='%(asctime)s %(message)s')

# Fetch Historical Data
def fetch_klines(symbol, interval, limit=1000):
    try:
        klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        if klines is None or len(klines) == 0:
            logging.error("No klines fetched")
            print("No klines fetched")
            return pd.DataFrame()
        
        logging.info(f"Fetched {len(klines)} klines")
        print(f"Fetched {len(klines)} klines")
        
        data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                             'close_time', 'quote_asset_volume', 'number_of_trades',
                                             'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
        data.set_index('timestamp', inplace=True)
        data['close'] = data['close'].astype(float)
        return data
    except Exception as e:
        logging.error(f"Error fetching klines: {e}")
        print(f"Error fetching klines: {e}")
        return pd.DataFrame()

# Calculate Moving Averages
def calculate_moving_averages(data, short_window=50, long_window=200):
    if len(data) < long_window:
        logging.warning("Not enough data to calculate long moving average")
        print("Not enough data to calculate long moving average")
        return data
    
    data['short_ma'] = data['close'].rolling(window=short_window).mean()
    data['long_ma'] = data['close'].rolling(window=long_window).mean()
    
    return data

# Define the Trading Logic
def check_for_crossover_and_trade(data, symbol, quantity):
    short_ma = data['short_ma'].iloc[-1]
    long_ma = data['long_ma'].iloc[-1]
    prev_short_ma = data['short_ma'].iloc[-2]
    prev_long_ma = data['long_ma'].iloc[-2]
    
    logging.info(f"Current Short MA: {short_ma}, Long MA: {long_ma}")
    print(f"Current Short MA: {short_ma}, Long MA: {long_ma}")
    logging.info(f"Previous Short MA: {prev_short_ma}, Previous Long MA: {prev_long_ma}")
    print(f"Previous Short MA: {prev_short_ma}, Previous Long MA: {prev_long_ma}")
    
    if pd.isna(short_ma) or pd.isna(long_ma) or pd.isna(prev_short_ma) or pd.isna(prev_long_ma):
        logging.warning("MA is NaN, skipping trade check")
        print("MA is NaN, skipping trade check")
        return
    
    if prev_short_ma < prev_long_ma and short_ma > long_ma:
        logging.info("Buy signal detected")
        print("Buy signal detected")
        place_order(symbol, 'BUY', 'MARKET', quantity)
    elif prev_short_ma > prev_long_ma and short_ma < long_ma:
        logging.info("Sell signal detected")
        print("Sell signal detected")
        place_order(symbol, 'SELL', 'MARKET', quantity)
    else:
        logging.info("No crossover detected")
        print("No crossover detected")

def place_order(symbol, side, order_type, quantity):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=order_type,
            quantity=quantity
        )
        logging.info(f"Order placed: {order}")
        print(f"Order placed: {order}")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

# Main Bot Logic
def run_bot():
    symbol = "BTCUSDT"
    interval = Client.KLINE_INTERVAL_5MINUTE
    quantity = 0.001  # Adjust based on your needs
    
    while True:
        try:
            logging.info("Fetching klines")
            print("Fetching klines")
            data = fetch_klines(symbol, interval)
            logging.info(f"Fetched {len(data)} klines")
            print(f"Fetched {len(data)} klines")
            
            if data.empty:
                logging.error("No data fetched, skipping this iteration")
                print("No data fetched, skipping this iteration")
                time.sleep(30)
                continue
            
            data = calculate_moving_averages(data)
            if 'short_ma' in data.columns and 'long_ma' in data.columns:
                check_for_crossover_and_trade(data, symbol, quantity)
            logging.info("Sleeping for 30 seconds")
            print("Sleeping for 30 seconds")
            time.sleep(30)  # Sleep for 30 seconds
        except Exception as e:
            logging.error(f"Error in bot loop: {e}")
            print(f"Error in bot loop: {e}")

if __name__ == "__main__":
    run_bot()
