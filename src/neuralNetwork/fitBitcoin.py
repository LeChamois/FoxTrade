import yfinance as yf
from TradeTools.main import NeuralNetwork

try:
    bot = NeuralNetwork.load('bitcoin')
except:
    bot = NeuralNetwork()

bot.save()