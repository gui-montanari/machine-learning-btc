from project_root.src.data_fetcher import DataFetcher
from project_root.src.indicators import Indicators
from project_root.src.recommendation_engine import RecommendationEngine
import logging
import numpy as np

class BitcoinAnalyzer:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.indicators = Indicators()
        self.recommendation_engine = RecommendationEngine()

    def run_analysis(self):
        real_time_price = self.data_fetcher.fetch_real_time_price()
        if not real_time_price:
            logging.error("Failed to fetch real-time price. Aborting analysis.")
            return

        if not self.data_fetcher.fetch_historical_data():
            logging.error("Failed to fetch historical data. Aborting analysis.")
            return

        self.indicators.set_data(self.data_fetcher.prices, self.data_fetcher.volumes)

        # Calculate indicators
        opening_price = self.data_fetcher.prices[-1]
        volume_ma = self.indicators.calculate_volume_ma()
        volatility = self.indicators.calculate_volatility()
        rsi = self.indicators.calculate_rsi()
        percentage_change = self.indicators.calculate_percentage_change()
        predicted_price = self.indicators.calculate_linear_regression()
        upper_band, lower_band = self.indicators.calculate_bollinger_bands()
        ema = self.indicators.calculate_ema()
        fib_levels = self.indicators.calculate_fibonacci_levels()
        macd, signal_macd = self.indicators.calculate_macd()
        adx = self.indicators.calculate_adx()
        stochastic = self.indicators.calculate_stochastic()
        tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b = self.indicators.calculate_ichimoku_cloud()

        # Get recommendations
        real_time_recommendation = self.recommendation_engine.get_recommendation(
            real_time_price, rsi, macd, signal_macd, fib_levels, senkou_span_a, senkou_span_b,
            ema, adx, stochastic, upper_band, lower_band, "real-time"
        )
        daily_recommendation = self.recommendation_engine.get_recommendation(
            opening_price, rsi, macd, signal_macd, fib_levels, senkou_span_a, senkou_span_b,
            ema, adx, stochastic, upper_band, lower_band, "daily"
        )

        # Print results
        self._print_analysis_results(
            real_time_price, opening_price, predicted_price, volume_ma, percentage_change,
            volatility, rsi, ema, lower_band, upper_band, fib_levels, senkou_span_a, senkou_span_b,
            real_time_recommendation, daily_recommendation
        )

    def _print_analysis_results(self, real_time_price, opening_price, predicted_price, volume_ma,
                                percentage_change, volatility, rsi, ema, lower_band, upper_band,
                                fib_levels, senkou_span_a, senkou_span_b, real_time_recommendation,
                                daily_recommendation):
        print(f"{'-'*70}\nBitcoin Analysis Results\n{'-'*70}")
        print(f"Real-time BTC Price (USD): ${real_time_price:.2f}")
        print(f"Opening BTC Price (USD): ${opening_price:.2f}")
        print(f"Predicted BTC Price (USD): ${predicted_price:.2f}")
        print(f"Last data timestamp: {self.data_fetcher.dates[-1]} Sao Paulo UTC -3")
        print(f"{'-'*70}")
        print(f"Volume MA (8 days, USD): ${volume_ma[-1]:.2f}b")
        print(f"Percentage Change (8 days): {percentage_change:.2f}%")
        print(f"Volatility: {volatility:.2f}")
        print(f"RSI (14 periods): {rsi[-1]:.2f}")
        print(f"EMA (8 periods, USD): ${ema[-1]:.2f}")
        print(f"Lower Bollinger Band (USD): ${lower_band:.2f}")
        print(f"Upper Bollinger Band (USD): ${upper_band:.2f}")
        print(f"Average price (last 30 periods): ${np.mean(self.data_fetcher.prices[-30:]):.2f}")
        print(f"Highest price (last 30 periods): ${np.max(self.data_fetcher.prices[-30:]):.2f}")
        print(f"Lowest price (last 30 periods): ${np.min(self.data_fetcher.prices[-30:]):.2f}")
        print(f"{'-'*70}\nFibonacci Levels (USD):")
        print(f"23.6% : ${fib_levels[0]:.2f}")
        print(f"38.2% : ${fib_levels[1]:.2f}")
        print(f"61.8% : ${fib_levels[2]:.2f}")
        print(f"{'-'*70}\nIchimoku Cloud:")
        print(f"Support (Senkou Span A): ${senkou_span_a:.2f}")
        print(f"Resistance (Senkou Span B): ${senkou_span_b:.2f}")
        print(f"Current Trend: {'Bullish' if real_time_price > senkou_span_b else 'Bearish' if real_time_price < senkou_span_a else 'Neutral'}")
        print(f"{'-'*70}\nReal-time Recommendation: {real_time_recommendation}\n{'-'*70}")
        print(f"{'-'*70}\nDaily Recommendation: {daily_recommendation}\n{'-'*70}")
