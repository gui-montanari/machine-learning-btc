import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class Indicators:
    def __init__(self):
        self.prices = []
        self.volumes = []

    def set_data(self, prices, volumes):
        self.prices = prices
        self.volumes = volumes

    def calculate_volume_ma(self, period=8):
        return np.convolve(self.volumes, np.ones(period), 'valid') / period / 1e9

    def calculate_percentage_change(self):
        if len(self.prices) < 9:
            raise ValueError("Insufficient price data.")
        return ((self.prices[-1] - self.prices[-9]) / self.prices[-9]) * 100

    def calculate_volatility(self, period=8):
        if len(self.prices) < period:
            raise ValueError(f"Insufficient price data. Need at least {period} prices.")
        returns = np.diff(np.log(self.prices[-period:]))
        return np.std(returns)

    def calculate_linear_regression(self, days_ahead=1):
        x = np.arange(len(self.prices)).reshape(-1, 1)
        y = np.array(self.prices)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        model = LinearRegression().fit(x_train, y_train)
        return model.predict(np.array([[len(self.prices) + days_ahead]]))[0]

    def calculate_rsi(self, period=14):
        deltas = np.diff(self.prices)
        seed = deltas[:period+1]
        up = seed[seed >= 0].sum()/period
        down = -seed[seed < 0].sum()/period
        rs = up/down
        rsi = np.zeros_like(self.prices)
        rsi[:period] = 100. - 100./(1. + rs)

        for i in range(period, len(self.prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.
            else:
                upval = 0.
                downval = -delta
            up = (up*(period-1) + upval)/period
            down = (down*(period-1) + downval)/period
            rs = up/down
            rsi[i] = 100. - 100./(1. + rs)
        return rsi

    def calculate_bollinger_bands(self, period=20, num_std=2):
        if len(self.prices) < period:
            raise ValueError(f"Insufficient price data. Need at least {period} prices.")
        ma = np.convolve(self.prices, np.ones(period), 'valid') / period
        std = [np.std(self.prices[i - period:i]) for i in range(period, len(self.prices) + 1)]
        upper_band = ma + num_std * np.array(std)
        lower_band = ma - num_std * np.array(std)
        return upper_band[-1], lower_band[-1]

    def calculate_ema(self, period=8):
        ema = np.zeros(len(self.prices))
        ema[0] = self.prices[0]
        multiplier = 2 / (period + 1)
        for i in range(1, len(self.prices)):
            ema[i] = (self.prices[i] * multiplier) + (ema[i-1] * (1 - multiplier))
        return ema

    def calculate_fibonacci_levels(self, period=8):
        if len(self.prices) < period:
            raise ValueError(f"Insufficient price data. Need at least {period} prices.")
        max_price = max(self.prices[-period:])
        min_price = min(self.prices[-period:])
        diff = max_price - min_price
        levels = [max_price - level * diff for level in [0.236, 0.382, 0.618]]
        return levels

    def calculate_macd(self, short=12, long=26, signal=9):
        ema_short = np.convolve(self.prices, np.ones(short), 'valid') / short
        ema_long = np.convolve(self.prices, np.ones(long), 'valid') / long
        macd = ema_short[-len(ema_long):] - ema_long
        signal_line = np.convolve(macd, np.ones(signal), 'valid') / signal
        return macd[-1], signal_line[-1]

    def calculate_adx(self, period=14):
        if len(self.prices) < period:
            raise ValueError(f"Insufficient price data. Need at least {period} prices.")
        tr = np.zeros(len(self.prices))
        dm_plus = np.zeros(len(self.prices))
        dm_minus = np.zeros(len(self.prices))
        for i in range(1, len(self.prices)):
            high_diff = self.prices[i] - self.prices[i-1]
            low_diff = self.prices[i-1] - self.prices[i]
            tr[i] = max(high_diff, low_diff, abs(self.prices[i] - self.prices[i-1]))
            dm_plus[i] = max(high_diff, 0)
            dm_minus[i] = max(low_diff, 0)
        atr = np.mean(tr[-period:])
        adx = 100 * np.mean(abs(dm_plus[-period:] - dm_minus[-period:]) / (dm_plus[-period:] + dm_minus[-period:]))
        return adx

    def calculate_stochastic(self, period=14):
        if len(self.prices) < period:
            raise ValueError(f"Insufficient price data. Need at least {period} prices.")
        low = np.min(self.prices[-period:])
        high = np.max(self.prices[-period:])
        return 100 * (self.prices[-1] - low) / (high - low)

    def calculate_ichimoku_cloud(self, tenkan_period=9, kijun_period=26, senkou_period=52):
        tenkan_sen = (np.max(self.prices[-tenkan_period:]) + np.min(self.prices[-tenkan_period:])) / 2
        kijun_sen = (np.max(self.prices[-kijun_period:]) + np.min(self.prices[-kijun_period:])) / 2
        senkou_span_a = (tenkan_sen + kijun_sen) / 2
        senkou_span_b = (np.max(self.prices[-senkou_period:]) + np.min(self.prices[-senkou_period:])) / 2
        return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b