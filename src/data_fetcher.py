import requests
from datetime import datetime
from pytz import timezone
from functools import lru_cache

class DataFetcher:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.currency = "usd"
        self.days = 365
        self.prices = []
        self.volumes = []
        self.dates = []

    @lru_cache(maxsize=1)
    def fetch_real_time_price(self):
        url = f"{self.base_url}/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": self.currency}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()["bitcoin"][self.currency]
        except requests.RequestException as e:
            print(f"Error fetching real-time BTC price: {e}")
            return None

    @lru_cache(maxsize=1)
    def fetch_historical_data(self):
        url = f"{self.base_url}/coins/bitcoin/market_chart"
        params = {"vs_currency": self.currency, "days": self.days}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            self.prices = [p[1] for p in data["prices"]]
            self.volumes = [v[1] for v in data["total_volumes"]]
            self.dates = [datetime.utcfromtimestamp(p[0] / 1000).astimezone(timezone('America/Sao_Paulo')).strftime('%Y-%m-%d %H:%M:%S') for p in data["prices"]]
            return True
        except requests.RequestException as e:
            print(f"Error fetching historical BTC data: {e}")
            return False