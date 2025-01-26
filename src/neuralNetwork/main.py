import json
import os
from typing import Generator, Literal
import keras
import numpy as np


TupleModel = tuple[keras.Sequential, keras.Sequential, keras.Sequential, keras.Sequential]

def getModel(vectors : int, vectorDimension : int = 500, outputLength : int = 50):
    model = keras.models.Sequential([
        keras.Input(shape = (vectorDimension * vectors,)),
        keras.layers.Dense(outputLength * 8, activation='relu'),
        keras.layers.Dense(outputLength * 4, activation='relu'),
        keras.layers.Dense(outputLength * 2, activation='relu'),
        keras.layers.Dense(outputLength, activation='relu'),
    ])
    return model

class NeuralNetwork():
    def __init__(
            self,
            inputDimension : int = 500,
            outputDimension : int = 50,
            models : TupleModel | None = None
            ):
        if models is None:
            self.secondModel = getModel(4, inputDimension, outputDimension)
            self.minuteModel = getModel(3, inputDimension, outputDimension)
            self.hourModel = getModel(2, inputDimension, outputDimension)
            self.dayModel = getModel(1, inputDimension, outputDimension)
            self.compile()
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
            seconds : list,
            minutes : list,
            hours : list,
            days : list,
            epochs : int = 100,
            batchSize : int = 32,
            ):
        if not(len(seconds) == len(minutes) == len(hours) == len(days) == self.inputDim+self.outputDim):
            raise ValueError('Length of inputs must match input dimension + output dimension')
        
        separator = self.inputDim
        Xseconds = seconds[:separator]
        Xminutes = minutes[:separator]
        Xhours = hours[:separator]
        Xdays = days[:separator]
        Yseconds = seconds[separator:]
        Yminutes = minutes[separator:]
        Yhours = hours[separator:]
        Ydays = days[separator:]


        self.secondModel.fit(
            np.array([Xseconds+Xminutes+Xhours+Xdays]),
            np.array([Yseconds]),
            epochs=epochs,
            batch_size=batchSize
        )
        self.minuteModel.fit(
            np.array([Xminutes+Xhours+Xdays]),
            np.array([Yminutes]),
            epochs=epochs,
            batch_size=batchSize
        )
        self.hourModel.fit(
            np.array([Xhours+Xdays]),
            np.array([Yhours]),
            epochs=epochs,
            batch_size=batchSize
        )
        self.dayModel.fit(
            np.array([Xdays]),
            np.array([Ydays]),
            epochs=epochs,
            batch_size=batchSize
        )
    
    def speedTrain(
            self,
            seconds : Generator[float, None, None],
            minutes : Generator[float, None, None],
            hours : Generator[float, None, None],
            days : Generator[float, None, None],
            ):
        
        i = 0
        SecondsX = []
        for value in seconds:
            SecondsX.append(value)
            i+=1
            if i >= self.inputDim:
                break
        SecondsY = []
        for value in seconds:
            SecondsY.append(value)
        
        i = 0
        MinutesX = []
        for value in minutes:
            SecondsX.append(value)
            MinutesX.append(value)
            i+=1
            if i >= self.inputDim:
                break
        MinutesY = []
        for value in minutes:
            SecondsY.append(value)
            MinutesY.append(value)

        i = 0
        HoursX = []
        for value in hours:
            SecondsX.append(value)
            MinutesX.append(value)
            HoursX.append(value)
            i+=1
            if i >= self.inputDim:
                break
        HoursY = []
        for value in hours:
            SecondsY.append(value)
            MinutesY.append(value)
            HoursY.append(value)
        
        i = 0
        DaysX = []
        for value in days:
            SecondsX.append(value)
            MinutesX.append(value)
            HoursX.append(value)
            DaysX.append(value)
            i+=1
            if i >= self.inputDim:
                break
        DaysY = []
        for value in days:
            SecondsY.append(value)
            MinutesY.append(value)
            HoursY.append(value)
            DaysY.append(value)
        
    
    def save(self, folderName):
        folderName = 'SavedBots/' + folderName
        os.makedirs(folderName, exist_ok=True)
        self.secondModel.save(f'{folderName}/secondModel.keras')
        self.minuteModel.save(f'{folderName}/minuteModel.keras')
        self.hourModel.save(f'{folderName}/hourModel.keras')
        self.dayModel.save(f'{folderName}/dayModel.keras')
        with open(f'{folderName}/config.json', 'w') as file:
            json.dump({
                'inputDimension': self.inputDim,
                'outputDimension': self.outputDim
            }, file)
    
    def load(folderName):
        folderName = 'SavedBots/' + folderName
        models = (
            keras.models.load_model(f'{folderName}/secondModel.keras', compile=False),
            keras.models.load_model(f'{folderName}/minuteModel.keras', compile=False),
            keras.models.load_model(f'{folderName}/hourModel.keras', compile=False),
            keras.models.load_model(f'{folderName}/dayModel.keras', compile=False),
        )
        with open(f'{folderName}/config.json', 'r') as config:
            config = json.load(config)
        return NeuralNetwork(models=models, **config).compile()
    
    def compile(self):
        for model in (self.secondModel, self.minuteModel, self.hourModel, self.dayModel):
            model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        return self