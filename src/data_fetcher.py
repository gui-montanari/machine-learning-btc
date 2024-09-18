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
        self.high_price = None
        self.low_price = None

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
            
            # Fetch daily high and low
            self._fetch_daily_high_low()
            
            return True
        except requests.RequestException as e:
            print(f"Error fetching historical BTC data: {e}")
            return False

    def _fetch_daily_high_low(self):
        url = f"{self.base_url}/coins/bitcoin/ohlc"
        params = {"vs_currency": self.currency, "days": 1}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            self.high_price = max(item[2] for item in data)  # High is the 3rd element
            self.low_price = min(item[3] for item in data)   # Low is the 4th element
        except requests.RequestException as e:
            print(f"Error fetching daily high/low BTC data: {e}")
            self.high_price = None
            self.low_price = None