import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import datetime
import math


import os



def ARIMA_ALGO(df,quote):

    # Check if the directory exists and create it if it doesn't
    directory = './my-react-app/build/graphs/'
    if not os.path.exists(directory):
        os.makedirs(directory)

    uniqueVals = df["Code"].unique()  
    len(uniqueVals)
    df=df.set_index("Code")
    #for daily basis
    def parser(x):
        return datetime.strptime(x, '%Y-%m-%d')
    def arima_model(train, test):
        history = [x for x in train]
        predictions = list()
        for t in range(len(test)):
            model = ARIMA(history, order=(6,1 ,0))
            model_fit = model.fit()
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)
        return predictions
    for company in uniqueVals[:10]:
        data=(df.loc[company,:]).reset_index()
        data['Price'] = data['Close']
        Quantity_date = data[['Price','Date']]
        Quantity_date.index = Quantity_date['Date'].map(lambda x: parser(x))
        Quantity_date['Price'] = Quantity_date['Price'].map(lambda x: float(x))
        Quantity_date = Quantity_date.fillna(Quantity_date.bfill())
        Quantity_date = Quantity_date.drop(['Date'],axis =1)
        fig = plt.figure(figsize=(7.2,4.8),dpi=65)
        plt.plot(Quantity_date)
        plt.savefig('./my-react-app/build/graphs/Trends.png')
        plt.close(fig)
        
        quantity = Quantity_date.values
        size = int(len(quantity) * 0.80)
        train, test = quantity[0:size], quantity[size:len(quantity)]
        #fit in model
        predictions = arima_model(train, test)
        
        #plot graph
        fig = plt.figure(figsize=(7.2,4.8),dpi=65)
        plt.plot(test,label='Actual Price')
        plt.plot(predictions,label='Predicted Price')
        plt.legend(loc=4)
        plt.savefig('./my-react-app/build/graphs/ARIMA.png')
        plt.close(fig)
        print()
        print("##############################################################################")
        arima_pred=predictions[-2]
        print("Tomorrow's",quote," Closing Price Prediction by ARIMA:",arima_pred)
        #rmse calculation
        error_arima = math.sqrt(mean_squared_error(test, predictions))
        # print("ARIMA RMSE:",error_arima)
        print("##############################################################################")
        return arima_pred, error_arima
    