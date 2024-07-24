from http import client
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print(data) # Log the received alert for debugging purposes
    # Process the alert and send a signal to the trading bot
    process_alert(data)
    return jsonify(success=True)


def process_alert(alert):
    signal = alert.get("signal")
    symbol = alert.get("symbol", "BTCUSDT") # Default to BTCUSDT if not specified
    quantity = 0.001 # Adjust the quantity based on your needs
    
    
    if signal == "long":
        execute_trade('buy', symbol, quantity)
    elif signal == "short":
        execute_trade('sell', symbol, quantity)
        

def execute_trade(signal, symbol, quantity):
    if signal == 'buy':
        order = client.order_market_buy(symbol=symbol, quantity=quantity)
    elif signal == 'sell':
        order = client.order_market_sell(symbol=symbol, quantity=quantity)
    else:
        return None
    
    return order 


if __name__ == '__main__':
    app.run(port=5000)