from termcolor import cprint
from mods.markets import get_historical_prices as getPrices

print(*getPrices('BTCUSDT', '1s', 20))



a = True
b = False

u = []
v = []
k = []

result = [a if e in k else b for e in (v if v is not k else u)]