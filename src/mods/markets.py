import yfinance as yf
from typing import Optional, Tuple, List, Dict
from datetime import datetime
import pandas as pd

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
    period: str = '1d',  # e.g. '1d', '5d', '1mo', '3mo'
) -> Tuple[List[datetime], List[float]]:
    """
    Get historical prices with custom interval and period
    
    Args:
        ticker: Stock symbol
        interval: Time between data points (Xs, Xm, Xh, Xd)
        period: Historical period to fetch
    
    Returns:
        Tuple of (dates, prices) lists
    """
    try:
        # Validate interval format
        if len(interval) < 2:
            raise ValueError("Invalid interval format")
            
        value = int(interval[:-1])
        unit = interval[-1]
        
        if unit not in VALID_INTERVALS:
            raise ValueError(f"Invalid interval unit. Must be one of: {list(VALID_INTERVALS.keys())}")
            
        if f"{value}{unit}" not in VALID_INTERVALS[unit]:
            raise ValueError(f"Invalid interval value for unit {unit}")
            
        if period not in VALID_PERIODS:
            raise ValueError(f"Invalid period. Must be one of: {VALID_PERIODS}")

        # Fetch data
        stock = yf.Ticker(ticker)
        history = stock.history(interval=interval, period=period)
        
        if history.empty:
            return ([], [])
            
        dates = history.index.tolist()
        prices = history['Close'].tolist()
        return (dates, prices)
        
    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {str(e)}")
        return ([], [])

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