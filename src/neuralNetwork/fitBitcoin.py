import yfinance as yf
from main import NeuralNetwork

try:
    bot = NeuralNetwork.load('bitcoin')
except:
    bot = NeuralNetwork()

yf.


bot.save()