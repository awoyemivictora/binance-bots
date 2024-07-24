import os
import time
import pandas as pd
from binance.client import Client
from binance.error import ClientError
from dotenv import load_dotenv
import ta
from flask import Flask, request, jsonify
import imaplib
import email
import threading
import logging

# Loading environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")  # This should be your app-specific password

# Initialize Binance client
client = Client(api_key, secret_key, testnet=True)

# Set up logging
logging.basicConfig(level=logging.INFO)

# Flask app for receiving TradingView alerts
app = Flask(__name__)

# Connect to email
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(email_user, email_pass)
mail.select('inbox')

def check_email():
    while True:
        try:
            status, messages = mail.search(None, 'UNSEEN')
            messages = messages[0].split()
            for msg_num in messages:
                status, msg_data = mail.fetch(msg_num, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode()
                                process_signal(body)
            time.sleep(60)
        except Exception as e:
            logging.error(f"Error checking email: {e}")

def process_signal(signal):
    if "BUY" in signal:
        place_order("BUY")
    elif "SELL" in signal:
        place_order("SELL")

def get_market_price(symbol):
    # Fetch the latest price for the symbol
    ticker = client.get_symbol_ticker(symbol=symbol)
    return float(ticker['price'])

def place_order(side):
    symbol = 'BTCUSDT'
    quantity = 0.001
    price = get_market_price(symbol)

    try:
        if side == "BUY":
            response = client.order_market_buy(symbol=symbol, quantity=quantity)
        elif side == "SELL":
            response = client.order_market_sell(symbol=symbol, quantity=quantity)
        logging.info(response)
    except ClientError as e:
        logging.error(f"An error occurred: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    logging.info(f"Received alert: {data}")
    process_alert(data)
    return jsonify(success=True)

def process_alert(alert):
    signal = alert.get("signal")
    symbol = alert.get("symbol", "BTCUSDT")  # Default to BTCUSDT if not specified
    quantity = 0.001  # Adjust the quantity based on your needs

    if signal == "long":
        execute_trade('buy', symbol, quantity)
    elif signal == "short":
        execute_trade('sell', symbol, quantity)

def execute_trade(signal, symbol, quantity):
    try:
        if signal == 'buy':
            order = client.order_market_buy(symbol=symbol, quantity=quantity)
        elif signal == 'sell':
            order = client.order_market_sell(symbol=symbol, quantity=quantity)
        logging.info(order)
        return order
    except ClientError as e:
        logging.error(f"Error executing trade: {e}")

def fetch_klines(symbol, interval, limit=1000):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    data = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
                                         'close_time', 'quote_asset_volume', 'number_of_trades',
                                         'taker_buy_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    data.set_index('timestamp', inplace=True)
    data['close'] = data['close'].astype(float)
    data['high'] = data['high'].astype(float)
    data['low'] = data['low'].astype(float)

    return data

def calculate_indicators(df):
    # Bollinger Bands
    df['bb_middle'] = ta.volatility.bollinger_mavg(df['close'], window=20)
    df['bb_upper'] = ta.volatility.bollinger_hband(df['close'], window=20, window_dev=2)
    df['bb_lower'] = ta.volatility.bollinger_lband(df['close'], window=20, window_dev=2)
    
    # Fibonacci Retracements
    max_price = df['high'].max()
    min_price = df['low'].min()
    df['fib_0'] = max_price
    df['fib_236'] = max_price - (max_price - min_price) * 0.236
    df['fib_382'] = max_price - (max_price - min_price) * 0.382
    df['fib_50'] = max_price - (max_price - min_price) * 0.50
    df['fib_618'] = max_price - (max_price - min_price) * 0.618
    df['fib_786'] = max_price - (max_price - min_price) * 0.786
    df['fib_100'] = min_price
    
    return df 

def trading_strategy(df):
    df['long_signal'] = (df['close'] < df['bb_lower']) & (df['close'] > df['fib_50'])
    df['short_signal'] = (df['close'] > df['bb_upper']) & (df['close'] < df['fib_50'])
    
    return df 

def run_bot():
    symbol = "BTCUSDT"
    interval = Client.KLINE_INTERVAL_1HOUR
    quantity = 0.001  # Adjust the quantity based on your needs
    while True:
        try:
            data = fetch_klines(symbol, interval)
            data = calculate_indicators(data)
            data = trading_strategy(data)
        
            if data['long_signal'].iloc[-1]:
                logging.info("Buy signal detected")
                execute_trade('buy', symbol, quantity)
            elif data['short_signal'].iloc[-1]:
                logging.info("Sell signal detected")
                execute_trade('sell', symbol, quantity)
                
            time.sleep(60 * 60)  # Run the bot every hour
        except Exception as e:
            logging.error(f"Error in bot loop: {e}")

def start_flask():
    app.run(port=5000)

if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.start()
    
    # Start the email checker in a separate thread
    email_thread = threading.Thread(target=check_email)
    email_thread.start()
    
    # Start the bot loop
    run_bot()
