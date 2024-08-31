
#**************** IMPORT PACKAGES ********************
from flask import Flask, jsonify, request, render_template, send_from_directory,url_for,make_response
from flask_cors import CORS 
import pandas as pd
import os
from datetime import datetime
import datetime as dt
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
import numpy as np
import json 
from bson.objectid import ObjectId


# Importing  modules
from algorithms.arima import ARIMA_ALGO
# from algorithms.lstm import LSTM_ALGO
from algorithms.linear_regression import LIN_REG_ALGO
from algorithms.sentiment_analysis import retrieve_news_polarity
from utils.get_data import get_historical
# from utils.load_config import load_config
from utils.mongodb_functions import check_email
from utils.mongodb_functions import update_document
from utils.mongodb_functions import create_document
from dotenv import load_dotenv
# Ignore Warnings
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__, static_folder='my-react-app/build', static_url_path='')
CORS(app) 

load_dotenv()
news_api_key = os.getenv('NEWS_API_KEY')

#mongodb credentials
mongo_uri = os.getenv('MONGO_URI')
database = os.getenv('MONGO_DATABASE')
collection = os.getenv('MONGO_COLLECTION')


@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')



@app.route('/mongodb_search_email', methods=['POST'])
def mongodb_search_email():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        if not email:
            return jsonify({"error": "Email is empty"}), 400

        checked_data, check = check_email(mongo_uri, database, collection, email)
        
        # Ensure the checked_data is in a proper JSON format
        if isinstance(checked_data, dict):  # If already a dictionary
            checked_data = checked_data
        else:  # If it's a JSON string
            checked_data = json.loads(checked_data)
        
        # Create a structured response
        response = {
            "data": checked_data,
            "status": check
        }
        return jsonify(response), 200


@app.route('/mongodb_update', methods=['POST'])
def mongodb_update():
    if request.is_json:
        data = request.get_json()
        # print(data)
        user_id_str = data.get('id')  # Extract the string ID from the dictionary
        company = data.get('company')
        date_time = data.get('dateTime')

        print(f"User ID from Frontend: {user_id_str}")

        updated_count = update_document(mongo_uri, database,collection, user_id_str, company, date_time)
        
        if updated_count > 0:
            return jsonify({"message": "History updated successfully"}), 200
        else:
            return jsonify({"error": "Failed to update history"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400

@app.route('/mongodb_create', methods=['POST'])
def mongodb_create():
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')
        company = data.get('company')
        date_time = data.get('dateTime')

        created_id=create_document(mongo_uri,database,collection,email,name,company,date_time)

        if created_id:
            return jsonify({"message": "New user created successfully", "user_id": str(created_id)}), 201
        else:
            return jsonify({"error": "Failed to create new user"}), 400
    else:
        return jsonify({"error": "Request must be JSON"}), 400





@app.route('/insertintotable', methods=['POST'])
def insertintotable():
    if request.is_json:
        data = request.get_json()
        nm = data.get('nm')
        company = data.get('company')
        if not nm or not company:
            return jsonify({"error": "Stock symbol or company is missing!"}), 400
        
        
    # Fetch and prepare the data
    quote=nm
    company=company

    #Try-except to check if valid stock symbol
    try:
        get_historical(quote)
    except:
        return render_template('index.html',not_found=True)
    
    else:
    
        #************** PREPROCESSUNG ***********************
        df = pd.read_csv('./stock_data/' + quote + '.csv')
        print("##############################################################################")
        print("Today's",quote,"Stock Data: ")
        today_stock=df.iloc[-1:]
        print(today_stock)
        print("##############################################################################")
        df = df.dropna()
        code_list=[]
        for i in range(0,len(df)):
            code_list.append(quote)
        df2=pd.DataFrame(code_list,columns=['Code'])
        df2 = pd.concat([df2, df], axis=1)
        df=df2


        # Running algorithms
        arima_pred, error_arima = ARIMA_ALGO(df,quote)
        # lstm_pred, error_lstm = LSTM_ALGO(df,quote)
        df, lr_pred, forecast_set, mean, error_lr = LIN_REG_ALGO(df,quote)
        polarity, article_list, pos, neg, neutral = retrieve_news_polarity(quote, company,news_api_key)
        # print("articles list",article_list)
        # Extract titles from articles
        titles = [article['title'] for article in article_list]
        def convert_numpy(obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()  # Convert arrays to lists
            elif isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                                np.int16, np.int32, np.int64, np.uint8,
                                np.uint16, np.uint32, np.uint64)):
                return int(obj)  # Convert numpy integers to Python int
            elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
                return float(obj)  # Convert numpy floats to Python float
            elif isinstance(obj, dict):
                return {key: convert_numpy(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            else:
                return obj

        # Prepare results including paths to generated graphs
        results = {
            "today_stock": df.iloc[-1].to_dict(),
            "predictions": {
                "arima": arima_pred,
                # "lstm": lstm_pred,
                "linear_regression": lr_pred
            },
            "forecast": forecast_set,
            "errors": {
                "arima_rmse": error_arima,
                # "lstm_rmse": error_lstm,
                "lr_rmse": error_lr
            },
            "sentiment_analysis": {
                "Polarity": polarity,
                "Positive": pos,
                "Negative": neg,
                "Neutral": neutral
            },
            "articles_titles": titles,
            "graph_images": {
                "arima": url_for('static', filename='graphs/ARIMA.png'),
                # "lstm": url_for('static', filename='graphs/LSTM.png'),
                "linear_regression": url_for('static', filename='graphs/LR.png'),
                "trends": url_for('static', filename='graphs/Trends.png'),                
                "sentiment_analysis": url_for('static', filename='graphs/SA.png')
            }
        }



        def handle_nan(obj):
            if isinstance(obj, float) and np.isnan(obj):
                return None  # Convert NaN to None, which will become 'null' in JSON
            elif isinstance(obj, dict):
                return {k: handle_nan(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [handle_nan(x) for x in obj]
            return obj

        results = convert_numpy(results)  # Ensure all numpy types are converted

        results = handle_nan(results)  # Ensure no NaNs remain

        # print("Final results ready for JSON serialization:", results)
        return jsonify(results)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)











