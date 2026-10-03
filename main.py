import os
import requests
import datetime as dt
from twilio.rest import Client

STOCK = "GOOG"
COMPANY_NAME = "Alphabet Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api = os.environ['ALPHAVANTAGE_API_KEY']
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api = os.environ['NEWSAPI_KEY']
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']

yesterday_date = dt.date.today() - dt.timedelta(1)
day_before_date = yesterday_date - dt.timedelta(1)

stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': stock_api
}

news_parameters = {
    'q': COMPANY_NAME,
    'from': day_before_date,
    'to': dt.date.today(),
    'sortBy': 'popularity',
    'apiKey': news_api
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()['Time Series (Daily)']
opening_price = float(data[str(yesterday_date)]['1. open'])
closing_price = float(data[str(day_before_date)]['4. close'])
highest_price = float(data[str(day_before_date)]['2. high'])
lowest_price = float(data[str(day_before_date)]['3. low'])
percentage = (((opening_price-closing_price)/closing_price)*100)

significant_change = False

if percentage > 0 or percentage < 0:
    significant_change = True

if percentage > 0:
    percentage = f'🔼{percentage:.2f}'
else:
    percentage = f'🔽{percentage:.2f}'

if significant_change:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()['articles'][:3]
    news = {item['title']: item['description'] for item in news_data}
    client = Client(account_sid, auth_token)
    for key in news:
        message = client.messages.create(
            body=f'open:{opening_price}\nclose:{closing_price}\nHigh:{highest_price}\nlow:{lowest_price}\n{STOCK}:{percentage}\n\nHeadline:{key}\n\nBrief:{news[key]}',
            from_=os.environ['TWILIO_FROM_NUMBER'],
            to=os.environ['ALERT_TO_NUMBER']
        )
        print(message.status)

