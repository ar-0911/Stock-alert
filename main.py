import requests
import datetime as dt
from twilio.rest import Client

STOCK = "GOOG"
COMPANY_NAME = "Alphabet Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
stock_api = "8JHN4CVWFTF2RV9K"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
news_api = "baeee10f119d49ebbd9a1266d889a06f"
account_sid = 'ACbbf7d75b34869fb9a70b984dd6f0ac9d'
auth_token = '8e7b7d674b9979601651e6bca7e679e9'

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
            from_='+19032731379',
            to='+918884230038'
        )
        print(message.status)

