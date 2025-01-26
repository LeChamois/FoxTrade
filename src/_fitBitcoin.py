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
        print(len(getPrices("BTCUSDT", '1s', 47520050)))
        #bot.train()
        if running:
            time.sleep(5)

bot.save('bitcoin')