from typing import Literal
import keras
import numpy as np

NeuralNetworkTupleOfModel = tuple[keras.Sequential, keras.Sequential, keras.Sequential, keras.Sequential]

def getModel(vectors : int, vectorDimension : int = 500, outputLength : int = 500):
    model = keras.models.Sequential([
        keras.Input(shape = (vectorDimension * vectors,)),
        keras.layers.Dense(outputLength * 8, activation='relu'),
        keras.layers.Dense(outputLength * 4, activation='relu'),
        keras.layers.Dense(outputLength * 2, activation='relu'),
        keras.layers.Dense(outputLength, activation='relu'),
    ])
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

class NeuralNetwork():
    def __init__(
            self,
            inputDimension : int = 50000,
            outputDimension : int = 500,
            models : keras.Sequential | None = None
            ):
        if models is None:
            self.secondModel = getModel(4, inputDimension, outputDimension)
            self.minuteModel = getModel(3, inputDimension, outputDimension)
            self.hourModel = getModel(2, inputDimension, outputDimension)
            self.dayModel = getModel(1, inputDimension, outputDimension)
        else:
            self.secondModel = models[0]
            self.minuteModel = models[1]
            self.hourModel = models[2]
            self.dayModel = models[3]

        self.inputDim = inputDimension
        self.outputDim = outputDimension

    def sellOnSecond(self):
        ...
    
    def sellOnMinute(self):
        ...

    def sellOnHour(self):
        ...
    
    def sellOnDay(self):
        ...
    
    def buyOnSecond(self):
        ...
    
    def buyOnMinute(self):
        ...
    
    def buyOnHour(self):
        ...
    
    def buyOnDay(self):
        ...
    
    def getSecondInputs(self) -> list | tuple:
        ...
    
    def getMinuteInputs(self) -> list | tuple:
        ...
    
    def getHourInputs(self) -> list | tuple:
        ...
    
    def getDayInputs(self) -> list | tuple:
        ...
    
    def use(self, timeLevel : Literal[0, 1, 2, 3]):
        dayInputs = self.getDayInputs()
        hourInputs = self.getHourInputs()
        minuteInputs = self.getMinuteInputs()
        secondInputs = self.getSecondInputs()

        secondOutputs = self.secondModel.predict(np.array([secondInputs+minuteInputs+hourInputs+dayInputs]))
        if sum(secondOutputs)/len(secondOutputs) > sum(secondInputs[:-10])/11:
            self.buyOnSecond()
        elif sum(secondOutputs)/len(secondOutputs) < sum(secondInputs[:-10])/9:
            self.sellOnSecond()

        if timeLevel > 0:
            minuteOutputs = self.minuteModel.predict(np.array([minuteInputs+hourInputs+dayInputs]))
            if sum(minuteOutputs)/len(minuteOutputs) > sum(minuteInputs[:-10])/11:
                self.buyOnMinute()
            elif sum(minuteOutputs)/len(minuteOutputs) < sum(minuteInputs[:-10])/9:
                self.sellOnMinute()

            if timeLevel > 1:
                hourOutputs = self.hourModel.predict(np.array([hourInputs+dayInputs]))
                if sum(hourOutputs)/len(hourOutputs) > sum(hourInputs[:-10])/11:
                    self.buyOnHour()
                elif sum(hourOutputs)/len(hourOutputs) < sum(hourInputs[:-10])/9:
                    self.sellOnHour()
                                                           

                if timeLevel > 2:
                    dayOutputs = self.dayModel.predict(np.array([dayInputs]))
                    if sum(dayOutputs)/len(dayOutputs) > sum(dayInputs[:-10])/11:
                        self.buyOnDay()
                    elif sum(dayOutputs)/len(dayOutputs) < sum(dayInputs[:-10])/9:
                        self.sellOnDay()
    
    def train(
            self,
            values : list[float],
            epochs : int = 100,
            batchSize : int = 32,
            ):
        totalTrainable = 1+len(values)-(86400 * (self.inputDim+self.outputDim))
        if totalTrainable < 0:
            raise ValueError('Not enough data to train')
        else:
            X = []
            Y = []
            for i in range(totalTrainable):
                sep = i+self.inputDim
                X.append(values[i : sep])
                Y.append(values[sep : sep+self.outputDim])
            
            X = np.array(X)
            Y = np.array(Y)
            
            self.secondModel.fit(X, Y, epochs=epochs, batch_size=batchSize)