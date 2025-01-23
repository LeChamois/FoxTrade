import keras
from termcolor import cprint
import neuralNetwork.main as main

main.getModel(4).save("file.keras")

model : keras.Sequential = keras.models.load_model("file.keras", compile=False)
model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])