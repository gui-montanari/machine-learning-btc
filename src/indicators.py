import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

class Indicators:
    def __init__(self):
        self.prices = []
        self.volumes = []

    def set_data(self, prices, volumes):
        self.prices = np.array(prices)
        self.volumes = np.array(volumes)

    def calculate_volume_ma(self, period=8):
        return np.convolve(self.volumes, np.ones(period), 'valid') / period / 1e9

    def calculate_percentage_change(self, period=8):
        if len(self.prices) < period + 1:
            raise ValueError(f"Insufficient price data. Need at least {period + 1} prices.")
        return ((self.prices[-1] - self.prices[-period-1]) / self.prices[-period-1]) * 100

    def calculate_volatility(self, period=8):
        if len(self.prices) < period:
            raise ValueError(f"Insufficient price data. Need at least {period} prices.")
        returns = np.diff(np.log(self.prices[-period:]))
        return np.std(returns) * np.sqrt(252)  # Annualized volatility

    def calculate_linear_regression(self, days_ahead=1):
        x = np.arange(len(self.prices)).reshape(-1, 1)
        y = self.prices
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
        model = LinearRegression().fit(x_train, y_train)
        return model.predict(np.array([[len(self.prices) + days_ahead]]))[0]

    def calculate_bollinger_bands(self, period=20, num_std=2):
        if len(self.prices) < period:
            raise ValueError(f"Insufficient price data. Need at least {period} prices.")
        ma = np.convolve(self.prices, np.ones(period), 'valid') / period
        std = np.array([np.std(self.prices[i - period:i]) for i in range(period, len(self.prices) + 1)])
        upper_band = ma + num_std * std
        lower_band = ma - num_std * std
        return upper_band[-1], lower_band[-1]

    def calculate_rsi(self, period=14):
        if len(self.prices) < period + 1:
            raise ValueError(f"Insufficient price data. Need at least {period + 1} prices.")
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

    def calculate_ema(self, period=8):
        if len(self.prices) < 2 * period:
            raise ValueError(f"Insufficient price data. Need at least {2 * period} prices.")
        ema = np.zeros_like(self.prices)
        ema[:period] = np.mean(self.prices[:period])
        multiplier = 2 / (period + 1)
        for i in range(period, len(self.prices)):
            ema[i] = (self.prices[i] - ema[i-1]) * multiplier + ema[i-1]
        return ema

    def calculate_fibonacci_levels(self, period=8):
        if len(self.prices) < period:
            raise ValueError(f"Insufficient price data. Need at least {period} prices.")
        max_price = np.max(self.prices[-period:])
        min_price = np.min(self.prices[-period:])
        diff = max_price - min_price
        levels = [max_price - level * diff for level in [0.236, 0.382, 0.618]]
        return levels

    def calculate_macd(self, short=12, long=26, signal=9):
        if len(self.prices) < long + signal:
            raise ValueError(f"Insufficient price data. Need at least {long + signal} prices.")
        ema_short = self.calculate_ema(short)
        ema_long = self.calculate_ema(long)
        macd = ema_short - ema_long
        signal_line = np.convolve(macd, np.ones(signal), 'valid') / signal
        return macd, signal_line

    def calculate_adx(self, period=14):
        if len(self.prices) < 2 * period:
            raise ValueError(f"Insufficient price data. Need at least {2 * period} prices.")
        high = np.array([max(self.prices[i-1:i+1]) for i in range(1, len(self.prices))])
        low = np.array([min(self.prices[i-1:i+1]) for i in range(1, len(self.prices))])
        close = self.prices[1:]
        
        up = high - np.roll(high, 1)
        down = np.roll(low, 1) - low
        
        plus_dm = np.where((up > down) & (up > 0), up, 0)
        minus_dm = np.where((down > up) & (down > 0), down, 0)
        
        tr = np.maximum(high - low, np.abs(high - np.roll(close, 1)), np.abs(low - np.roll(close, 1)))
        
        plus_di = 100 * np.convolve(plus_dm, np.ones(period), 'valid') / np.convolve(tr, np.ones(period), 'valid')
        minus_di = 100 * np.convolve(minus_dm, np.ones(period), 'valid') / np.convolve(tr, np.ones(period), 'valid')
        
        dx = 100 * np.abs(plus_di - minus_di) / (plus_di + minus_di)
        adx = np.convolve(dx, np.ones(period), 'valid') / period
        
        return adx[-1], plus_di[-1], minus_di[-1]

    def calculate_stochastic(self, period=14, k_period=3, d_period=3):
        if len(self.prices) < period + k_period + d_period:
            raise ValueError(f"Insufficient price data. Need at least {period + k_period + d_period} prices.")
        low_min = np.array([np.min(self.prices[i-period:i]) for i in range(period, len(self.prices))])
        high_max = np.array([np.max(self.prices[i-period:i]) for i in range(period, len(self.prices))])
        
        k_fast = 100 * (self.prices[period:] - low_min) / (high_max - low_min)
        k = np.convolve(k_fast, np.ones(k_period), 'valid') / k_period
        d = np.convolve(k, np.ones(d_period), 'valid') / d_period
        
        return k[-1]

    def calculate_ichimoku_cloud(self, tenkan_period=9, kijun_period=26, senkou_period=52, chikou_period=26):
        if len(self.prices) < max(tenkan_period, kijun_period, senkou_period, chikou_period):
            raise ValueError(f"Insufficient price data. Need at least {max(tenkan_period, kijun_period, senkou_period, chikou_period)} prices.")
        
        tenkan_sen = (np.max(self.prices[-tenkan_period:]) + np.min(self.prices[-tenkan_period:])) / 2
        kijun_sen = (np.max(self.prices[-kijun_period:]) + np.min(self.prices[-kijun_period:])) / 2
        senkou_span_a = (tenkan_sen + kijun_sen) / 2
        senkou_span_b = (np.max(self.prices[-senkou_period:]) + np.min(self.prices[-senkou_period:])) / 2
        
        return tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b

    def analyze_volume(self, period=20):
        volume_ma = np.mean(self.volumes[-period:])
        current_volume = self.volumes[-1]
        volume_change = (current_volume - volume_ma) / volume_ma * 100
        return volume_change

    def identify_divergence(self, indicator, period=14):
        price_change = self.prices[-1] - self.prices[-period]
        indicator_change = indicator[-1] - indicator[-period]
        
        if price_change > 0 and indicator_change < 0:
            return "Bearish divergence detected"
        elif price_change < 0 and indicator_change > 0:
            return "Bullish divergence detected"
        else:
            return "No divergence detected"

    def calculate_on_balance_volume(self):
        obv = np.zeros(len(self.prices))
        obv[0] = self.volumes[0]
        for i in range(1, len(self.prices)):
            if self.prices[i] > self.prices[i-1]:
                obv[i] = obv[i-1] + self.volumes[i]
            elif self.prices[i] < self.prices[i-1]:
                obv[i] = obv[i-1] - self.volumes[i]
            else:
                obv[i] = obv[i-1]
        return obv

    def calculate_money_flow_index(self, period=14):
        typical_price = (self.prices + np.roll(self.prices, 1) + np.roll(self.prices, 2)) / 3
        raw_money_flow = typical_price * self.volumes
    
        positive_flow = np.where(typical_price > np.roll(typical_price, 1), raw_money_flow, 0)
        negative_flow = np.where(typical_price < np.roll(typical_price, 1), raw_money_flow, 0)
    
        positive_mf = np.sum(positive_flow[-period:])
        negative_mf = np.sum(negative_flow[-period:])
    
        if negative_mf == 0:
            return 100  # If negative money flow is zero, MFI is 100
    
        mfi = 100 - (100 / (1 + positive_mf / negative_mf))
        return mfi

    def calculate_pivot_points(self):
        if len(self.prices) < 2:
            raise ValueError("Insufficient price data for Pivot Points calculation")
        
        high = max(self.prices[-2:])
        low = min(self.prices[-2:])
        close = self.prices[-1]
        
        pivot = (high + low + close) / 3
        r1 = (2 * pivot) - low
        s1 = (2 * pivot) - high
        r2 = pivot + (high - low)
        s2 = pivot - (high - low)
        r3 = high + 2 * (pivot - low)
        s3 = low - 2 * (high - pivot)
        
        return [pivot, r1, s1, r2, s2, r3, s3]