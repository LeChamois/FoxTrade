import json
import os
from typing import Literal
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
        if totalTrainable < 1:
            raise ValueError(
                f"""
                Not enough data to train.
                given : {len(values)+1}
                required : {86400 * (self.inputDim+self.outputDim)}
                {-totalTrainable} values missing
                """
                )
        else:
            XSeconds = []
            YSeconds = []
            XMinutes = []
            YMinutes = []
            XHours = []
            YHours = []
            XDays = []
            YDays = []
            for i in range(totalTrainable):

                sep = i+self.inputDim
                XSeconds.append(values[i : sep])
                YSeconds.append(values[sep : sep+self.outputDim])

                XMinutes.append([])
                YMinutes.append([])
                sep = i+(self.inputDim*60)
                for j in range(i, sep, 60):
                    XMinutes[-1].append(values[j])
                for j in range(sep, sep+(self.outputDim*60), 60):
                    YMinutes[-1].append(values[j])
                
                XHours.append([])
                YHours.append([])
                sep = i+(self.inputDim*3600)
                for j in range(i, sep, 3600):
                    XHours[-1].append(values[j])
                for j in range(sep, sep+(self.outputDim*3600), 3600):
                    YHours[-1].append(values[j])
                
                XDays.append([])
                YDays.append([])
                sep = i+(self.inputDim*86400)
                for j in range(i, sep, 86400):
                    XDays[-1].append(values[j])
                for j in range(sep, sep+(self.outputDim*86400), 86400):
                    YDays[-1].append(values[j])

            
            self.secondModel.fit(
                np.array([
                    XSeconds[i] + XMinutes[i] + XHours[i] + XDays[i] for i in range(totalTrainable)
                ]),
                np.array([
                    YSeconds[i] + YMinutes[i] + YHours[i] + YDays[i] for i in range(totalTrainable)
                ]),
                epochs=epochs, batch_size=batchSize
            )
            
            self.minuteModel.fit(
                np.array([
                    XMinutes[i] + XHours[i] + XDays[i] for i in range(totalTrainable)
                ]),
                np.array([
                    YMinutes[i] + YHours[i] + YDays[i] for i in range(totalTrainable)
                ]),
                epochs=epochs, batch_size=batchSize
            )
            
            self.hourModel.fit(
                np.array([
                    XHours[i] + XDays[i] for i in range(totalTrainable)
                ]),
                np.array([
                    YHours[i] + YDays[i] for i in range(totalTrainable)
                ]),
                epochs=epochs, batch_size=batchSize
            )

            self.dayModel.fit(
                np.array(XDays),
                np.array(YDays),
                epochs=epochs, batch_size=batchSize
            )
    
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
        for model in models:
            model.compile(loss='mean_squared_error', optimizer='adam', metrics=['accuracy'])
        with open(f'{folderName}/config.json', 'r') as config:
            config = json.load(config)
        return NeuralNetwork(models=models, **config)