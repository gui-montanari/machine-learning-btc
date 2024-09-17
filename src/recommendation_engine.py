import numpy as np

class RecommendationEngine:
    def get_recommendation(self, price, rsi, macd, signal_macd, fib_levels, senkou_span_a, senkou_span_b,
                           ema, adx, stochastic, upper_band, lower_band, timeframe):
        buy_signals, sell_signals = self._calculate_signals(
            price, rsi, macd, signal_macd, fib_levels, senkou_span_a, senkou_span_b,
            ema, adx, stochastic, upper_band, lower_band
        )
        
        suggested_buy_price, buy_reason = self._calculate_suggested_buy_price(price, lower_band, fib_levels)
        suggested_sell_price, sell_reason = self._calculate_suggested_sell_price(price, upper_band, fib_levels)
        
        return self._generate_recommendation(buy_signals, sell_signals, suggested_buy_price, suggested_sell_price,
                                             buy_reason, sell_reason, price, timeframe)

    def _calculate_signals(self, price, rsi, macd, signal_macd, fib_levels, senkou_span_a, senkou_span_b,
                           ema, adx, stochastic, upper_band, lower_band):
        buy_signals = 0
        sell_signals = 0
        
        # RSI
        if rsi[-1] < 30:
            buy_signals += 2
        elif rsi[-1] < 40:
            buy_signals += 1
        elif rsi[-1] > 70:
            sell_signals += 2
        elif rsi[-1] > 60:
            sell_signals += 1
        
        # MACD
        if macd > signal_macd:
            buy_signals += 1
            if macd > 0:
                buy_signals += 1
        else:
            sell_signals += 1
            if macd < 0:
                sell_signals += 1
        
        # Fibonacci Levels
        if price < fib_levels[0]:  # Below 23.6% level
            buy_signals += 2
        elif price < fib_levels[1]:  # Below 38.2% level
            buy_signals += 1
        elif price > fib_levels[2]:  # Above 61.8% level
            sell_signals += 2
        elif price > fib_levels[1]:  # Above 38.2% level
            sell_signals += 1
        
        # Ichimoku Cloud
        if price > senkou_span_b:
            buy_signals += 1
            if price > senkou_span_a:
                buy_signals += 1
        elif price < senkou_span_a:
            sell_signals += 1
            if price < senkou_span_b:
                sell_signals += 1
        
        # EMA
        if price > ema[-1]:
            buy_signals += 1
        else:
            sell_signals += 1
        
        # ADX (trend strength)
        if adx > 25:  # Strong trend
            if buy_signals > sell_signals:
                buy_signals += 2
            else:
                sell_signals += 2
        
        # Stochastic Oscillator
        if stochastic < 20:
            buy_signals += 2
        elif stochastic < 30:
            buy_signals += 1
        elif stochastic > 80:
            sell_signals += 2
        elif stochastic > 70:
            sell_signals += 1
        
        # Bollinger Bands
        if price < lower_band:
            buy_signals += 2
        elif price > upper_band:
            sell_signals += 2
        
        return buy_signals, sell_signals

    def _calculate_suggested_buy_price(self, price, lower_band, fib_levels):
        support_level = max(lower_band, fib_levels[0])
        avg_price = np.mean(price)  # Assuming price is a list of recent prices
        std_dev = np.std(price)
        
        if price < support_level:
            suggested_price = max(price * 0.99, price - std_dev)
            reason = "The current price is below the support level, indicating a potential buying opportunity. Suggested price factors in recent volatility."
        elif price < avg_price - std_dev:
            suggested_price = (price + support_level) / 2
            reason = "The price is significantly below the recent average, but above support. We suggest a price between current and support levels."
        elif price < avg_price:
            suggested_price = price * 0.995  # 0.5% below current price
            reason = "The price is below the recent average. A slight discount to the current price is suggested."
        else:
            suggested_price = avg_price - std_dev
            reason = "The price is above the recent average. We suggest waiting for a pullback to the lower end of the recent price range."

        return suggested_price, reason

    def _calculate_suggested_sell_price(self, price, upper_band, fib_levels):
        resistance_level = min(upper_band, fib_levels[2])
        avg_price = np.mean(price)  # Assuming price is a list of recent prices
        std_dev = np.std(price)
        
        if price > resistance_level:
            suggested_price = min(price * 1.01, price + std_dev)
            reason = "The current price is above the resistance level, indicating a potential selling opportunity. Suggested price factors in recent volatility."
        elif price > avg_price + std_dev:
            suggested_price = (price + resistance_level) / 2
            reason = "The price is significantly above the recent average, but below resistance. We suggest a price between current and resistance levels."
        elif price > avg_price:
            suggested_price = price * 1.005  # 0.5% above current price
            reason = "The price is above the recent average. A slight premium to the current price is suggested."
        else:
            suggested_price = avg_price + std_dev
            reason = "The price is below the recent average. We suggest waiting for a rise to the upper end of the recent price range."

        return suggested_price, reason

    def _generate_recommendation(self, buy_signals, sell_signals, suggested_buy_price, suggested_sell_price,
                                 buy_reason, sell_reason, price, timeframe):
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
