import numpy as np
from typing import List, Tuple

class RecommendationEngine:
    def get_recommendation(self, price: float, rsi: List[float], macd: float, signal_macd: float, 
                           fib_levels: List[float], senkou_span_a: float, senkou_span_b: float,
                           ema: List[float], adx: float, stochastic: float, upper_band: float, 
                           lower_band: float, timeframe: str, historical_prices: List[float]) -> str:
        buy_signals, sell_signals = self._calculate_signals(
            price, rsi, macd, signal_macd, fib_levels, senkou_span_a, senkou_span_b,
            ema, adx, stochastic, upper_band, lower_band
        )
        
        support, resistance = self._identify_support_resistance(price, lower_band, upper_band, fib_levels, senkou_span_a, senkou_span_b, historical_prices, timeframe)
        suggested_buy_price, buy_reason = self._calculate_suggested_buy_price(price, support, resistance)
        suggested_sell_price, sell_reason = self._calculate_suggested_sell_price(price, support, resistance)
        profit_target, profit_reason = self._calculate_profit_target(suggested_buy_price, resistance)
        
        trend_analysis = self._analyze_trend(historical_prices, timeframe)
        
        return self._generate_recommendation(buy_signals, sell_signals, suggested_buy_price, suggested_sell_price,
                                             buy_reason, sell_reason, price, timeframe, support, resistance, 
                                             trend_analysis, profit_target, profit_reason)

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

    def _identify_support_resistance(self, price, lower_band, upper_band, fib_levels, senkou_span_a, senkou_span_b, historical_prices, timeframe):
        if timeframe == "real-time" or timeframe == "daily":
            return self._identify_short_term_support_resistance(price, lower_band, upper_band, fib_levels, senkou_span_a, senkou_span_b)
        elif timeframe == "weekly":
            return self._identify_weekly_support_resistance(historical_prices)
        elif timeframe == "monthly":
            return self._identify_monthly_support_resistance(historical_prices)
        else:
            return self._identify_short_term_support_resistance(price, lower_band, upper_band, fib_levels, senkou_span_a, senkou_span_b)

    def _identify_short_term_support_resistance(self, price, lower_band, upper_band, fib_levels, senkou_span_a, senkou_span_b):
        support_levels = [lower_band, fib_levels[0], senkou_span_a]  # 23.6% Fib level and Senkou Span A
        resistance_levels = [upper_band, fib_levels[2], senkou_span_b]  # 61.8% Fib level and Senkou Span B
        
        support = max([level for level in support_levels if level < price], default=min(support_levels))
        resistance = min([level for level in resistance_levels if level > price], default=max(resistance_levels))
        
        return support, resistance

    def _identify_weekly_support_resistance(self, historical_prices):
        weekly_prices = historical_prices[-28::7]  # Last 4 weeks of data
        support = min(weekly_prices)
        resistance = max(weekly_prices)
        return support, resistance

    def _identify_monthly_support_resistance(self, historical_prices):
        monthly_prices = historical_prices[-90::30]  # Last 3 months of data
        support = min(monthly_prices)
        resistance = max(monthly_prices)
        return support, resistance

    def _calculate_suggested_buy_price(self, price, support, resistance):
        avg_price = (support + resistance) / 2
        
        if price < support:
            suggested_price = min(price * 1.01, support)  # 1% above current price or at support, whichever is lower
            reason = f"The current price (${price:.2f}) is below the identified support level (${support:.2f}). " \
                     f"This might indicate a potential buying opportunity, but be cautious of further downside."
        elif price < avg_price:
            suggested_price = (price + support) / 2
            reason = f"The price (${price:.2f}) is between the support (${support:.2f}) and the average price (${avg_price:.2f}). " \
                     f"Consider buying near the support level for a potentially better entry point."
        else:
            suggested_price = support
            reason = f"The current price (${price:.2f}) is above the average price (${avg_price:.2f}). " \
                     f"It might be prudent to wait for a pullback to the support level (${support:.2f}) before buying."

        return suggested_price, reason

    def _calculate_suggested_sell_price(self, price, support, resistance):
        avg_price = (support + resistance) / 2
        
        if price > resistance:
            suggested_price = max(price * 0.99, resistance)  # 1% below current price or at resistance, whichever is higher
            reason = f"The current price (${price:.2f}) is above the identified resistance level (${resistance:.2f}). " \
                     f"This might indicate a potential selling opportunity, but be aware of possible further upside."
        elif price > avg_price:
            suggested_price = (price + resistance) / 2
            reason = f"The price (${price:.2f}) is between the average price (${avg_price:.2f}) and the resistance (${resistance:.2f}). " \
                     f"Consider selling near the resistance level for a potentially better exit point."
        else:
            suggested_price = resistance
            reason = f"The current price (${price:.2f}) is below the average price (${avg_price:.2f}). " \
                     f"It might be beneficial to wait for a rise to the resistance level (${resistance:.2f}) before selling."

        return suggested_price, reason

    def _calculate_profit_target(self, buy_price, resistance):
        profit_percentage = 0.1  # 10% profit target
        profit_target = buy_price * (1 + profit_percentage)
        
        if profit_target > resistance:
            profit_target = resistance
            reason = f"The profit target is set at the resistance level (${profit_target:.2f}) to maximize potential gains while respecting market structure."
        else:
            reason = f"The profit target is set at {profit_percentage*100}% above the suggested buy price, aiming for a balanced risk-reward ratio."
        
        return profit_target, reason

    def _analyze_trend(self, historical_prices: List[float], timeframe: str) -> str:
        if timeframe == "real-time" or timeframe == "daily":
            return self._analyze_short_term_trend(historical_prices)
        elif timeframe == "weekly":
            return self._analyze_weekly_trend(historical_prices)
        elif timeframe == "monthly":
            return self._analyze_monthly_trend(historical_prices)
        else:
            return "Unknown timeframe for trend analysis."

    def _analyze_short_term_trend(self, prices: List[float]) -> str:
        short_ma = np.mean(prices[-7:])
        long_ma = np.mean(prices[-30:])
        current_price = prices[-1]
        
        if current_price > short_ma > long_ma:
            return "The short-term trend is bullish, with prices above both short and long-term moving averages."
        elif current_price < short_ma < long_ma:
            return "The short-term trend is bearish, with prices below both short and long-term moving averages."
        elif short_ma > long_ma:
            return "The short-term trend is potentially bullish, with the short-term moving average above the long-term moving average."
        else:
            return "The short-term trend is potentially bearish, with the short-term moving average below the long-term moving average."

    def _analyze_weekly_trend(self, prices: List[float]) -> str:
        weekly_returns = [(prices[i] - prices[i-7])/prices[i-7] for i in range(7, len(prices), 7)]
        avg_weekly_return = np.mean(weekly_returns)
        
        if avg_weekly_return > 0.05:
            return "The weekly trend is strongly bullish, with an average weekly return above 5%."
        elif avg_weekly_return > 0.02:
            return "The weekly trend is moderately bullish, with an average weekly return between 2% and 5%."
        elif avg_weekly_return > 0:
            return "The weekly trend is slightly bullish, with a positive average weekly return."
        elif avg_weekly_return > -0.02:
            return "The weekly trend is slightly bearish, with a small negative average weekly return."
        elif avg_weekly_return > -0.05:
            return "The weekly trend is moderately bearish, with an average weekly return between -2% and -5%."
        else:
            return "The weekly trend is strongly bearish, with an average weekly return below -5%."

    def _analyze_monthly_trend(self, prices: List[float]) -> str:
        monthly_returns = [(prices[i] - prices[i-30])/prices[i-30] for i in range(30, len(prices), 30)]
        avg_monthly_return = np.mean(monthly_returns)
        
        if avg_monthly_return > 0.15:
            return "The monthly trend is strongly bullish, with an average monthly return above 15%."
        elif avg_monthly_return > 0.07:
            return "The monthly trend is moderately bullish, with an average monthly return between 7% and 15%."
        elif avg_monthly_return > 0:
            return "The monthly trend is slightly bullish, with a positive average monthly return."
        elif avg_monthly_return > -0.07:
            return "The monthly trend is slightly bearish, with a small negative average monthly return."
        elif avg_monthly_return > -0.15:
            return "The monthly trend is moderately bearish, with an average monthly return between -7% and -15%."
        else:
            return "The monthly trend is strongly bearish, with an average monthly return below -15%."

    def _generate_recommendation(self, buy_signals, sell_signals, suggested_buy_price, suggested_sell_price,
                                 buy_reason, sell_reason, price, timeframe, support, resistance, 
                                 trend_analysis, profit_target, profit_reason):
        total_signals = buy_signals + sell_signals
        
        timeframe_str = "current moment" if timeframe == "real-time" else timeframe
        
        recommendation = f"Analysis for the {timeframe_str}:\n"
        recommendation += f"Current price: ${price:.2f}\n"
        recommendation += f"Identified support: ${support:.2f}\n"
        recommendation += f"Identified resistance: ${resistance:.2f}\n\n"
        recommendation += f"Trend Analysis: {trend_analysis}\n\n"

        if total_signals == 0:
            recommendation += "No clear signals detected. The market appears to be in a neutral state.\n"
        else:
            buy_percentage = (buy_signals / total_signals) * 100
            sell_percentage = (sell_signals / total_signals) * 100
            
            if buy_percentage >= 70:
                recommendation += f"Strong buy signal. {buy_percentage:.1f}% of indicators suggest an upward trend.\n"
            elif sell_percentage >= 70:
                recommendation += f"Strong sell signal. {sell_percentage:.1f}% of indicators suggest a downward trend.\n"
            elif buy_percentage >= 60:
                recommendation += f"Moderate buy signal. {buy_percentage:.1f}% of indicators lean towards an upward trend.\n"
            elif sell_percentage >= 60:
                recommendation += f"Moderate sell signal. {sell_percentage:.1f}% of indicators lean towards a downward trend.\n"
            else:
                recommendation += f"No clear trend. Buy signals: {buy_percentage:.1f}%, Sell signals: {sell_percentage:.1f}%.\n"

        recommendation += f"\nBuy consideration:\n"
        recommendation += f"Suggested buy near: ${suggested_buy_price:.2f}\n"
        recommendation += f"Reason: {buy_reason}\n"
        recommendation += f"Profit target: ${profit_target:.2f}\n"
        recommendation += f"Profit target reason: {profit_reason}\n"
        
        recommendation += f"\nSell consideration:\n"
        recommendation += f"Suggested sell near: ${suggested_sell_price:.2f}\n"
        recommendation += f"Reason: {sell_reason}\n"

        return recommendation