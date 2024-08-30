import React from 'react';
import './Dashboard.css';

function Dashboard({ data }) {
  console.log("Graph URLs:", data.graph_images);  // This will print all graph URLs to the console

  return (
    <div className="dashboard">
      <div className="stock-info">
        <h1>Stock Information for {data.today_stock.Code}</h1>
        <p>Date: {data.today_stock.Date}</p>
        <p>Open: {data.today_stock.Open}</p>
        <p>High: {data.today_stock.High}</p>
        <p>Low: {data.today_stock.Low}</p>
        <p>Close: {data.today_stock.Close}</p>
        <p>Volume: {data.today_stock.Volume}</p>
      </div>

      <div className="trends">
        <h2>Recent Trends in the Stock</h2>
        <img src={data.graph_images.trends} alt="Trend Analysis Graph" />
      </div>

      <div className="predictions">
        <h2>Predictions</h2>
        <div className="model">
          <h3>ARIMA Model</h3>
          <p>Today's prediction from ARIMA: {data.predictions.arima}</p>
          <img src={data.graph_images.arima} alt="ARIMA Prediction Graph" />
        </div>
        <div className="model">
          <h3>Linear Regression Model</h3>
          <p>Today's prediction from Linear Regression: {data.predictions.linear_regression}</p>
          <img src={data.graph_images.linear_regression} alt="Linear Regression Graph" />
        </div>
        {/* <div className="model">
          <h3>LSTM Model</h3>
          <p>Today's prediction from LSTM: {data.predictions.lstm}</p>
          <img src={data.graph_images.lstm} alt="LSTM Prediction Graph" />
        </div> */}
      </div>

      <div className="sentiment-analysis">
        <h2>Sentiment Analysis</h2>
        <p>Polarity: {data.sentiment_analysis.Polarity}</p>
        <p>Positive: {data.sentiment_analysis.Positive}</p>
        <p>Negative: {data.sentiment_analysis.Negative}</p>
        <p>Neutral: {data.sentiment_analysis.Neutral}</p>
        <img src={data.graph_images.sentiment_analysis} alt="Sentiment Analysis Graph" />
      </div>

      <div className="articles">
        <h2>Recent News</h2>
        <ul>
          {data.articles_titles.map(title => (
            <li key={title}>{title}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;

