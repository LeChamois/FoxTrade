import yfinance as yf
from typing import Generator, Optional, Tuple, List, Dict
from datetime import datetime
import pandas as pd
import requests

VALID_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']
VALID_INTERVALS = {
    's': ['1s', '5s', '15s', '30s'],
    'm': ['1m', '5m', '15m', '30m'],
    'h': ['1h', '2h', '4h', '6h'],
    'd': ['1d', '5d']
}

def get_historical_prices(
    ticker: str,
    interval: str,  # e.g. '1m', '5m', '1h', '1d'
    limit: int = 1000,
) ->  Generator[float, None, None]:

    # Endpoint de l'API Binance pour les données de chandeliers
    url = "https://api.binance.com/api/v3/klines"

    params = {
        "symbol": ticker,
        "interval": interval,
        "limit": limit  # Nombre de points de données
    }

    response = requests.get(url, params=params)

    data = response.json()
    
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume", 
        "close_time", "quote_asset_volume", "number_of_trades", 
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    for value in df["close"]:
        yield float(value)

def get_stock_price(ticker: str, period: str = '1d') -> Optional[float]:
    """Get current stock price from Yahoo Finance"""
    try:
        if period not in VALID_PERIODS:
            raise ValueError(f"Invalid period. Must be one of {VALID_PERIODS}")
        
        stock = yf.Ticker(ticker)
        history = stock.history(period=period)
        
        if history.empty:
            return None
            
        return float(history['Close'].iloc[-1])
        
    except Exception as e:
        print(f"Error fetching price for {ticker}: {str(e)}")
        return None

def get_monthly_prices(ticker: str) -> Tuple[List[datetime], List[float]]:
    """Get daily prices for the last month"""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period='1mo')
        
        if history.empty:
            return ([], [])
            
        dates = history.index.tolist()
        prices = history['Close'].tolist()
        return (dates, prices)
        
    except Exception as e:
        print(f"Error fetching monthly data for {ticker}: {str(e)}")
        return ([], [])

def get_stock_info(ticker: str) -> Optional[Dict]:
    """Get detailed stock information"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'name': info.get('longName', ''),
            'sector': info.get('sector', ''),
            'market_cap': info.get('marketCap', 0),
            'volume': info.get('volume', 0),
            'pe_ratio': info.get('trailingPE', 0),
            'dividend_yield': info.get('dividendYield', 0)
        }
    except Exception as e:
        print(f"Error fetching info for {ticker}: {str(e)}")
        return None

def test_market_functions():
    """Test market data functions"""
    symbol = 'AAPL'
    print(f"\nTesting market functions with {symbol}")
    
    print("\nCurrent price:")
    print(get_stock_price(symbol))
    
    print("\nMonthly prices:")
    dates, prices = get_monthly_prices(symbol)
    for date, price in zip(dates[-5:], prices[-5:]):
        print(f"{date.strftime('%Y-%m-%d')}: ${price:.2f}")
    
    print("\nStock info:")
    info = get_stock_info(symbol)
    if info:
        for key, value in info.items():
            print(f"{key}: {value}")

if __name__ == "__main__":
    test_market_functions()