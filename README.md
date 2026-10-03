# Stock Alert

A small Python job that watches a stock's daily move and texts you the top news headlines when it changes, a pocket-sized take on a Bloomberg terminal alert.

## How it works

1. Pulls daily prices for a ticker (default `GOOG`) from the [Alpha Vantage](https://www.alphavantage.co) `TIME_SERIES_DAILY` API.
2. Compares yesterday's open with the previous day's close to get the percentage move.
3. If the price moved, fetches the three most popular articles about the company from [NewsAPI](https://newsapi.org).
4. Sends each headline with open, close, high, low and the 🔼/🔽 change as an SMS via [Twilio](https://www.twilio.com).

## Run it

```bash
pip install -r requirements.txt
export ALPHAVANTAGE_API_KEY=… NEWSAPI_KEY=…
export TWILIO_ACCOUNT_SID=… TWILIO_AUTH_TOKEN=…
export TWILIO_FROM_NUMBER=+1… ALERT_TO_NUMBER=+91…
python main.py
```

Change `STOCK` and `COMPANY_NAME` at the top of `main.py` to track a different company. Schedule it daily with cron or a cloud scheduler.
