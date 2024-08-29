

    #************* LSTM SECTION **********************
import torch
import torch.nn as nn
from torch.autograd import Variable
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import math
from torch.utils.data import DataLoader, TensorDataset
from math import sqrt


class LSTMModel(nn.Module):
    def __init__(self):
        super(LSTMModel, self).__init__()
        self.lstm1 = nn.LSTM(input_size=1, hidden_size=50, batch_first=True)
        self.dropout1 = nn.Dropout(0.1)
        self.lstm2 = nn.LSTM(50, 50, batch_first=True)
        self.dropout2 = nn.Dropout(0.1)
        self.lstm3 = nn.LSTM(50, 50, batch_first=True)
        self.dropout3 = nn.Dropout(0.1)
        self.lstm4 = nn.LSTM(50, 50, batch_first=True)
        self.dropout4 = nn.Dropout(0.1)
        self.fc = nn.Linear(50, 1)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x = self.dropout1(x)
        x, _ = self.lstm2(x)
        x = self.dropout2(x)
        x, _ = self.lstm3(x)
        x = self.dropout3(x)
        x, _ = self.lstm4(x)
        x = self.dropout4(x)
        x = self.fc(x[:, -1, :])
        return x

def LSTM_ALGO(df,quote):
    # Splitting the dataset
    dataset_train = df.iloc[0:int(0.8 * len(df)), :]
    dataset_test = df.iloc[int(0.8 * len(df)):, :]
    training_set = dataset_train.iloc[:, 4:5].values  # Assuming 'Close' price is the 5th column

    # Feature Scaling
    scaler = MinMaxScaler(feature_range=(0, 1))
    training_set_scaled = scaler.fit_transform(training_set)

    # Creating data structure with 7 timesteps and 1 output
    X_train = []
    y_train = []
    for i in range(7, len(training_set_scaled)):
        X_train.append(training_set_scaled[i-7:i, 0])
        y_train.append(training_set_scaled[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)


    X_forecast=np.array(X_train[-1,1:])
    X_forecast=np.append(X_forecast,y_train[-1])
    X_forecast=np.reshape(X_forecast, (1,X_forecast.shape[0],1))





    # PyTorch Dataset
    train_data = TensorDataset(torch.Tensor(X_train), torch.Tensor(y_train))
    train_loader = DataLoader(train_data, batch_size=32, shuffle=False)

    # Model
    model = LSTMModel()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Training the model
    model.train()
    for epoch in range(25):
        for sequences, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(sequences)
            loss = criterion(outputs, labels.unsqueeze(1))
            loss.backward()
            optimizer.step()
        # print(f'Epoch {epoch+1}, Loss: {loss.item()}')

    # Predicting for the test set
    model.eval()
    dataset_total = np.concatenate((training_set_scaled, scaler.transform(dataset_test.iloc[:, 4:5].values)))
    inputs = dataset_total[len(dataset_total) - len(dataset_test) - 7:]
    X_test = []
    for i in range(7, len(inputs)):
        X_test.append(inputs[i-7:i, 0])
    X_test = np.array(X_test)
    X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)
    X_test = torch.Tensor(X_test)

    predicted_stock_price = model(X_test).detach().numpy()
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)

    # Real stock price
    real_stock_price = dataset_test.iloc[:, 4:5].values

    # Calculate RMSE
    error_lstm = sqrt(mean_squared_error(real_stock_price, predicted_stock_price))
    # print("LSTM RMSE:", error_lstm)

    # Plotting the results
    fig = plt.figure(figsize=(7.2,4.8),dpi=65)
    plt.plot(real_stock_price,label='Actual Price')  
    plt.plot(predicted_stock_price,label='Predicted Price')
        
    plt.legend(loc=4)
    plt.savefig('./my-react-app/build/graphs/LSTM.png')
    plt.close(fig)


    X_forecast = torch.tensor(X_forecast, dtype=torch.float32)  # Assuming X_forecast is already prepared
    # print(np.shape(X_forecast))
    forecasted_stock_price = model(X_forecast).detach().numpy()  # Predict the next step
    forecasted_stock_price = scaler.inverse_transform(forecasted_stock_price)



    # Extract the specific predicted price
    lstm_pred = forecasted_stock_price[0, 0]

    print("\n##############################################################################")
    print("Tomorrow's Closing Price Prediction by LSTM: ", lstm_pred)
    print("LSTM RMSE: ", error_lstm)
    print("##############################################################################")

    return lstm_pred, error_lstm
