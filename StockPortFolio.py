import requests
import pandas as pd
import matplotlib.pyplot as plt
API_KEY="7VKA3JPLU70ZMEUP"
portfolio={}
def add_stock(symbol,shares):
    shares=int(shares)
    symbol=symbol.upper()
    portfolio[symbol]=portfolio.get(symbol,0)+shares
    print(f"Added {shares} shares of {symbol} to the portfolio")

def remove_stock(symbol, shares):
    """Remove a stock from the portfolio."""
    shares = int(shares)
    symbol = symbol.upper()  
    if symbol in portfolio:
        if portfolio[symbol] >= shares:
            portfolio[symbol] -= shares
            if portfolio[symbol] == 0:
                del portfolio[symbol]
            print(f"Removed {shares} shares of {symbol} from the portfolio.")
        else:
            print(f"Cannot remove {shares} shares of {symbol} as you only own {portfolio[symbol]} shares.")
    else:
        print(f"{symbol} is not found in the portfolio.")
def get_stock_data(symbol):
    url=f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={API_KEY}"
    response=requests.get(url)
    data=response.json()
    return data

def get_stock_price(symbol):
    data=get_stock_data(symbol)
    if 'Time Series (1min)' in data:
        latest_time=sorted(data['Time Series (1min)'].keys())[-1]
        return float(data['Time Series (1min)'][latest_time]['4. close'])
    else:
        print(f"Failed to retrived data for {symbol}")
        return None
def track_portfolio():
    total_value=0
    for symbol,shares in portfolio.items():
        price=get_stock_price(symbol)
        if price is not None:
            total_value+=price*shares 
            print(f"{symbol}:{shares} shares at ${price} each.")
    print(f"Total portfolio value: ${total_value}")


action=input("Enter the action add/remove Stocks : ").strip()
stock=input("Enter the Symbol and Shares : ").split()
symbol,shares=stock[0],stock[1]
if action=='add':
    add_stock(symbol,shares)  
else:
    remove_stock(symbol,shares)
track_portfolio()