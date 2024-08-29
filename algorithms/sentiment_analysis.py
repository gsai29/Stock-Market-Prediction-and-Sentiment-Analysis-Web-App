
#**************** SENTIMENT ANALYSIS **************************
import pandas as pd
import requests
from datetime import datetime, timedelta
from textblob import TextBlob
import matplotlib.pyplot as plt
import numpy as np


def retrieve_news_polarity(symbol,company_name,news_api_key):

    url = "https://newsapi.org/v2/everything"
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    params = {
        "apiKey": news_api_key,
        "q": company_name,
        "language": "en",
        "from": start_date,
        "to": end_date,
        "sortBy": "publishedAt",
        "pageSize": 10 # Fetch 5 articles
    }
    
    # Fetch news articles
    response = requests.get(url, params=params)
    articles = response.json()['articles']
    print("articles are",articles)
    # Analyze sentiment
    pos, neg, neutral = 0, 0, 0
    article_list, polarities = [], []
    for article in articles:
        text = f"{article['title']} {article['description']}"
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        polarities.append(polarity)
        if polarity > 0:
            pos += 1
        elif polarity < 0:
            neg += 1
        else:
            neutral += 1
        article_list.append((text, polarity))
    
    # Calculate global polarity
    global_polarity = sum(polarities) / len(polarities) if polarities else 0
    
    # Visualization
    labels = ['Positive', 'Negative', 'Neutral']
    sizes = [pos, neg, neutral]

    print("sizes are",sizes)

    # Check if all sizes are zero or if any element is NaN
    if all(x == 0 for x in sizes) or any(np.isnan(x) for x in sizes):
        print("Warning: No valid sentiment data to plot.")
        sizes = [1]  # Create a dummy size to show a placeholder in the pie chart
        labels = ['No Data']
        explode = [0]  # No explosion since only one segment
    else:
        explode = (0.1, 0, 0)  # Explode the 'Positive' slice if it exists

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    plt.savefig('./my-react-app/build/graphs/SA.png')
    plt.close()

    return global_polarity, articles, pos, neg, neutral