from dotenv import load_dotenv
from newsapi import NewsApiClient
import os
import requests

load_dotenv()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
url = 'https://www.alphavantage.co/query'
parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': os.environ.get('PRICE_API_KEY')
}

response = requests.get(url, params=parameters)
response.raise_for_status()
stock_prices = response.json()['Time Series (Daily)']
prices = []
dates = []

for i, j in enumerate(stock_prices):
    dates.append(j)
    prices.append(float(stock_prices[j]['4. close']))
    if i == 1:
        break

if abs(prices[0] - prices[1]) / prices[1] > 0.05:
    news_api = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))

    all_articles = news_api.get_everything(
        q='Tesla',
        from_param=dates[1],
        to=dates[0],
        language='en',
        sort_by='relevancy',
    )['articles'][:3]

# STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

