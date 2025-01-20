import yfinance as yf
from typing import Optional, Tuple, List
from datetime import datetime
import pandas as pd

VALID_PERIODS = ['1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max']

def get_stock_price(ticker: str, ) -> Optional[float]:
    """Get current stock price from Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        history = stock.history(period='1d')
        
        if history.empty:
            return None
            
        return float(history['Close'].iloc[-1])
        
    except Exception as e:
        print(f"Error fetching price for {ticker}: {str(e)}")
        return None

def get_monthly_prices(ticker: str) -> Tuple[List[datetime], List[float]]:
    """
    Get daily prices for the last month
    
    Args:
        ticker: Stock symbol (e.g. 'AAPL')
    
    Returns:
        Tuple containing (dates list, prices list)
    """
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

if __name__ == "__main__":
    # Test current price
    price = get_stock_price('AAPL')
    print(f"Current AAPL price: {price}")
    
    # Test monthly data
    dates, prices = get_monthly_prices('AAPL')
    for date, price in zip(dates, prices):
        print(f"{date.strftime('%Y-%m-%d')}: ${price:.2f}")