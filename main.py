from dotenv import load_dotenv
from newsapi import NewsApiClient
from twilio.rest import Client
import os
import requests

load_dotenv()
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

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

increment = (prices[0] - prices[1]) / prices[1]

if abs(increment) >= 0.05:
    news_api = NewsApiClient(api_key=os.environ.get('NEWS_API_KEY'))
    body_message = ''

    all_articles = news_api.get_everything(
        q=COMPANY_NAME,
        from_param=dates[1],
        to=dates[0],
        language='en',
        sort_by='relevancy',
    )['articles'][:3]

    for article in all_articles:
        body_message += f'Headline: {article["title"]}\n' \
                        f'Brief: {article["description"]}\n' \
                        f'Read more: {article["url"]}\n' \
                        f'Published: {article["publishedAt"]}\n\n'

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    if increment < 0:
        symbol = '🔻'
    else:
        symbol = '🔺'

    message = client.messages.create(
        body=f'{STOCK}: {symbol}{round(increment * 100, 2)}%\n' + body_message.rstrip(),
        from_=os.environ.get('VIRTUAL_PHONE'),
        to=os.environ.get('PHONE_NUMBER')
    )


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height 
of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to 
file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height 
of the coronavirus market crash.
"""
