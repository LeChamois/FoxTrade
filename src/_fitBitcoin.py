import time

from termcolor import cprint
from mods.markets import get_historical_prices as getPrices
from neuralNetwork.main import NeuralNetwork
from pynput import keyboard as kb


try:
    bot = NeuralNetwork.load('bitcoin')
except:
    bot = NeuralNetwork()

running = True

def listen(key : kb.Key):
    global running
    if key == kb.Key.esc:
        cprint("Training will stop at the end of this session. Please wait.", 'magenta')
        running = False
        return False

with kb.Listener(listen) as listener:
    cprint("Training in progress. Press ESC to stop.", 'yellow')


    while running:
        cprint("new training session started.", 'cyan')
        bot.train(
            list(getPrices("BTCUSDT", '1s', 550)),
            list(getPrices("BTCUSDT", '1m', 550)),
            list(getPrices("BTCUSDT", '1h', 550)),
            list(getPrices("BTCUSDT", '1d', 550)),
        )
        """bot.speedTrain(
            getPrices("BTCUSDT", '1s', 550),
            getPrices("BTCUSDT", '1m', 550),
            getPrices("BTCUSDT", '1h', 550),
            getPrices("BTCUSDT", '1d', 550),
        )"""
        if running:
            time.sleep(5)

bot.save('bitcoin')
cprint('Bot successfully trained', 'magenta')