# Stock Market Prediction and Sentiment Analysis Web App

This repository contains a full-stack application designed to predict stock market trends and analyze sentiment from financial news. It integrates various technologies including Flask, React, MongoDB, and machine learning algorithms.

## Overview

The application serves as a tool for investors and financial analysts to gauge market sentiment and predict future stock prices using historical data and news sentiment analysis. It leverages advanced machine learning models to provide insights and visualizations that aid in making informed investment decisions.

## Features

- **Stock Prediction**: Utilizes ARIMA, and Linear Regression models to forecast future stock prices based on historical data.
- **Sentiment Analysis**: Analyzes the sentiment of financial news articles related to specific stocks using NLP techniques to determine market sentiment.
- **Interactive Dashboard**: A React-based frontend that displays predictions, sentiment analysis results, and historical data charts.
- **Data Management**: Backend API built with Flask to handle data processing and serve the frontend.
- **User History**: Keeps track of user history based on email id, and shows their search history during current search.

## Tech Stack

- **Frontend**: React, Chart.js
- **Backend**: Flask
- **Database**: MongoDB
- **Machine Learning**: Python, Pandas, Scikit-learn, Keras
- **APIs**: NewsAPI for fetching recent news articles

## Getting Started

### Prerequisites

- Node.js
- Python 3.x
- MongoDB
- Flask

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/gsai29/Stock-Market-Prediction-and-Sentiment-Analysis-Web-App.git
   cd stock-market-prediction-and-sentiment-analysis
   ```
2. **Install Python dependencies**

   ```bash
    pip install -r requirements.txt
    ```
    
3. **Set up the React application**

    Navigate to the React application directory:

   ```bash
    cd my-react-app
    ```
    
    Install Node.js dependencies and build the application:

   ```bash
    npm install
    npm run build
    ```
    
    Navigate back to the main directory:

   ```bash
    cd ..
    ```
    
4. ***Start the application***

    Run the Flask application which also serves the React frontend:

   ```bash
    python application.py
    ```
    
## Live Link
The project is deployed on AWS Elastic Beanstalk. Feel free to check it out - http://stock-env.eba-yb8tcmkf.us-west-2.elasticbeanstalk.com/ .


