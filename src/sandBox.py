import mods.markets as markets
import yfinance as yf


print(markets.get_historical_prices('BTC-USD', '1s', '5d'))
