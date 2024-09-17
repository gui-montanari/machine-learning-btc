from data_fetcher import DataFetcher
from indicators import Indicators
import logging

class BitcoinAnalyzer:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.indicators = Indicators()

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

        real_time_recommendation = self.provide_recommendation(real_time_price, "real-time")
        daily_recommendation = self.provide_recommendation(opening_price, "daily")

        # Print results
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
        print(f"Average price (last 30 periods): ${sum(self.data_fetcher.prices[-30:]) / 30:.2f}")
        print(f"Highest price (last 30 periods): ${max(self.data_fetcher.prices[-30:]):.2f}")
        print(f"Lowest price (last 30 periods): ${min(self.data_fetcher.prices[-30:]):.2f}")
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

    def provide_recommendation(self, price, timeframe):
        fib_levels = self.indicators.calculate_fibonacci_levels()
        rsi = self.indicators.calculate_rsi()
        ema = self.indicators.calculate_ema()
        tenkan_sen, kijun_sen, senkou_span_a, senkou_span_b = self.indicators.calculate_ichimoku_cloud()
        macd, signal_macd = self.indicators.calculate_macd()
        adx = self.indicators.calculate_adx()
        stochastic = self.indicators.calculate_stochastic()
        upper_band, lower_band = self.indicators.calculate_bollinger_bands()
        
        buy_signals = 0
        sell_signals = 0
        
        # RSI
        if rsi[-1] < 30:
            buy_signals += 1
        elif rsi[-1] > 70:
            sell_signals += 1
        
        # MACD
        if macd > signal_macd:
            buy_signals += 1
        else:
            sell_signals += 1
        
        # Fibonacci Levels
        if price < fib_levels[0]:  # Below 23.6% level
            buy_signals += 1
        elif price > fib_levels[2]:  # Above 61.8% level
            sell_signals += 1
        
        # Ichimoku Cloud
        if price > senkou_span_b:
            buy_signals += 1
        elif price < senkou_span_a:
            sell_signals += 1
        
        # EMA
        if price > ema[-1]:
            buy_signals += 1
        else:
            sell_signals += 1
        
        # ADX (trend strength)
        if adx > 25:  # Strong trend
            if buy_signals > sell_signals:
                buy_signals += 1
            else:
                sell_signals += 1
        
        # Stochastic Oscillator
        if stochastic < 20:
            buy_signals += 1
        elif stochastic > 80:
            sell_signals += 1
        
        # Bollinger Bands
        if price < lower_band:
            buy_signals += 1
        elif price > upper_band:
            sell_signals += 1
        
        # Calculate suggested prices
        suggested_buy_price, buy_reason = self.calculate_suggested_buy_price(price, lower_band, fib_levels)
        suggested_sell_price, sell_reason = self.calculate_suggested_sell_price(price, upper_band, fib_levels)
        
        # Final recommendation
        total_signals = buy_signals + sell_signals
        
        timeframe_str = "current moment" if timeframe == "real-time" else "today"
        
        if total_signals == 0:
            return f"No clear signals for the {timeframe_str}. The market appears to be in a neutral state. " \
                   f"Monitor the market closely. Current price: ${price:.2f}\n" \
                   f"Potential buy near: ${suggested_buy_price:.2f}, potential sell near: ${suggested_sell_price:.2f}\n" \
                   f"Buy reason: {buy_reason}\nSell reason: {sell_reason}"
        
        buy_percentage = (buy_signals / total_signals) * 100
        sell_percentage = (sell_signals / total_signals) * 100
        
        if buy_percentage >= 70:
            return f"Strong buy signal for the {timeframe_str}. {buy_percentage:.1f}% of indicators suggest an upward trend. " \
                   f"Suggested buy price: ${suggested_buy_price:.2f}\nReason: {buy_reason}"
        elif sell_percentage >= 70:
            return f"Strong sell signal for the {timeframe_str}. {sell_percentage:.1f}% of indicators suggest a downward trend. " \
                   f"Suggested sell price: ${suggested_sell_price:.2f}\nReason: {sell_reason}"
        elif buy_percentage >= 60:
            return f"Moderate buy signal for the {timeframe_str}. {buy_percentage:.1f}% of indicators lean towards an upward trend. " \
                   f"Consider buying near: ${suggested_buy_price:.2f}\nReason: {buy_reason}"
        elif sell_percentage >= 60:
            return f"Moderate sell signal for the {timeframe_str}. {sell_percentage:.1f}% of indicators lean towards a downward trend. " \
                   f"Consider selling near: ${suggested_sell_price:.2f}\nReason: {sell_reason}"
        else:
            return f"No clear trend for the {timeframe_str}. Buy signals: {buy_percentage:.1f}%, Sell signals: {sell_percentage:.1f}%. " \
                   f"Monitor the market. Potential buy near: ${suggested_buy_price:.2f}, potential sell near: ${suggested_sell_price:.2f}\n" \
                   f"Buy reason: {buy_reason}\nSell reason: {sell_reason}"

    def calculate_suggested_buy_price(self, price, lower_band, fib_levels):
        support_level = max(lower_band, fib_levels[0])
        avg_price = sum(self.data_fetcher.prices[-30:]) / 30  # Média dos últimos 30 preços
        
        if price < support_level:
            suggested_price = price * 0.99  # 1% abaixo do preço atual
            reason = "O preço atual está abaixo do nível de suporte, indicando uma possível oportunidade de compra."
        elif price < avg_price:
            suggested_price = (price + support_level) / 2
            reason = "O preço está abaixo da média recente, mas acima do suporte. Sugerimos um preço entre o atual e o suporte."
        else:
            suggested_price = support_level
            reason = "O preço está acima da média recente. Sugerimos aguardar uma queda até o nível de suporte."

        return suggested_price, reason

    def calculate_suggested_sell_price(self, price, upper_band, fib_levels):
        resistance_level = min(upper_band, fib_levels[2])
        avg_price = sum(self.data_fetcher.prices[-30:]) / 30  # Média dos últimos 30 preços
        
        if price > resistance_level:
            suggested_price = price * 1.01  # 1% acima do preço atual
            reason = "O preço atual está acima do nível de resistência, indicando uma possível oportunidade de venda."
        elif price > avg_price:
            suggested_price = (price + resistance_level) / 2
            reason = "O preço está acima da média recente, mas abaixo da resistência. Sugerimos um preço entre o atual e a resistência."
        else:
            suggested_price = resistance_level
            reason = "O preço está abaixo da média recente. Sugerimos aguardar uma subida até o nível de resistência."

        return suggested_price, reason