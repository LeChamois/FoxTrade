from termcolor import cprint
from mods.markets import get_historical_prices as getPrices

print(*getPrices('BTCUSDT', '1s', 20))