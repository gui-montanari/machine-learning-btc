import numpy as np
from typing import List

class RecommendationEngine:
    def get_recommendation(self, price: float, rsi: List[float], macd: List[float], signal_macd: List[float], 
                        fib_levels: List[float], senkou_span_a: float, senkou_span_b: float,
                        ema: List[float], adx: float, di_plus: float, di_minus: float, stochastic: float, 
                        upper_band: float, lower_band: float, timeframe: str, historical_prices: List[float],
                        historical_volumes: List[float], pivot_points: List[float]) -> str:
        buy_signals, sell_signals = self._calculate_signals(
            price, rsi, macd, signal_macd, fib_levels, senkou_span_a, senkou_span_b,
            ema, adx, di_plus, di_minus, stochastic, upper_band, lower_band
        )
        
        support, resistance = self._identify_support_resistance(price, lower_band, upper_band, fib_levels, senkou_span_a, senkou_span_b, historical_prices, timeframe, pivot_points)
        suggested_buy_price, buy_reason = self._calculate_suggested_buy_price(price, support, resistance)
        suggested_sell_price, sell_reason = self._calculate_suggested_sell_price(price, support, resistance)
        profit_target, profit_reason = self._calculate_profit_target(suggested_buy_price, resistance)
        stop_loss, stop_loss_reason = self._calculate_stop_loss(suggested_buy_price, support)
        
        trend_analysis = self._analyze_trend(historical_prices, timeframe, adx, di_plus, di_minus)
        
        # Calculate period-specific indicators
        if timeframe == "real-time" or timeframe == "daily":
            period = 1
        elif timeframe == "weekly":
            period = 7
        elif timeframe == "monthly":
            period = 30
        else:
            period = 1

        volume_change = self._calculate_volume_change(historical_volumes, period)
        rsi_divergence = self._identify_divergence(historical_prices, rsi, period)
        macd_divergence = self._identify_divergence(historical_prices, macd, period)
        mfi = self._calculate_mfi(historical_prices, historical_volumes, period)
        
        return self._generate_recommendation(buy_signals, sell_signals, suggested_buy_price, suggested_sell_price,
                                            buy_reason, sell_reason, price, timeframe, support, resistance, 
                                            trend_analysis, profit_target, profit_reason, stop_loss, stop_loss_reason,
                                            volume_change, rsi_divergence, macd_divergence, mfi)

    def _calculate_signals(self, price, rsi, macd, signal_macd, fib_levels, senkou_span_a, senkou_span_b,
                           ema, adx, di_plus, di_minus, stochastic, upper_band, lower_band):
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
        if macd[-1] > signal_macd[-1]:
            buy_signals += 1
            if macd[-1] > 0:
                buy_signals += 1
        else:
            sell_signals += 1
            if macd[-1] < 0:
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
        
        # ADX
        if adx > 25:
            if di_plus > di_minus:
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

    def _identify_support_resistance(self, price, lower_band, upper_band, fib_levels, senkou_span_a, senkou_span_b, historical_prices, timeframe, pivot_points):
        pivot, r1, s1, r2, s2, r3, s3 = pivot_points
        
        if timeframe == "real-time" or timeframe == "daily":
            support_levels = [lower_band, fib_levels[0], senkou_span_a, s1, s2]
            resistance_levels = [upper_band, fib_levels[2], senkou_span_b, r1, r2]
        elif timeframe == "weekly":
            support_levels = [min(historical_prices[-28::7]), s1, s2]  # Last 4 weeks of data
            resistance_levels = [max(historical_prices[-28::7]), r1, r2]
        elif timeframe == "monthly":
            support_levels = [min(historical_prices[-90::30]), s2, s3]  # Last 3 months of data
            resistance_levels = [max(historical_prices[-90::30]), r2, r3]
        else:
            support_levels = [lower_band, fib_levels[0], senkou_span_a, s1, s2]
            resistance_levels = [upper_band, fib_levels[2], senkou_span_b, r1, r2]
        
        support = max([level for level in support_levels if level < price], default=min(support_levels))
        resistance = min([level for level in resistance_levels if level > price], default=max(resistance_levels))
        
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

    def _calculate_stop_loss(self, buy_price, support):
        stop_loss_percentage = 0.05  # 5% stop loss
        stop_loss = buy_price * (1 - stop_loss_percentage)
        
        if stop_loss < support:
            stop_loss = support
            reason = f"The stop loss is set at the support level (${stop_loss:.2f}) to minimize potential losses while respecting market structure."
        else:
            reason = f"The stop loss is set at {stop_loss_percentage*100}% below the suggested buy price, aiming for a balanced risk-reward ratio."
        
        return stop_loss, reason

    def _analyze_trend(self, historical_prices: List[float], timeframe: str, adx: float, di_plus: float, di_minus: float) -> str:
        if timeframe == "real-time" or timeframe == "daily":
            return self._analyze_short_term_trend(historical_prices, adx, di_plus, di_minus)
        elif timeframe == "weekly":
            return self._analyze_weekly_trend(historical_prices, adx, di_plus, di_minus)
        elif timeframe == "monthly":
            return self._analyze_monthly_trend(historical_prices, adx, di_plus, di_minus)
        else:
            return "Unknown timeframe for trend analysis."

    def _analyze_short_term_trend(self, prices: List[float], adx: float, di_plus: float, di_minus: float) -> str:
        short_ma = np.mean(prices[-7:])
        long_ma = np.mean(prices[-30:])
        current_price = prices[-1]
        
        trend = ""
        if current_price > short_ma > long_ma:
            trend = "The short-term trend is bullish, with prices above both short and long-term moving averages."
        elif current_price < short_ma < long_ma:
            trend = "The short-term trend is bearish, with prices below both short and long-term moving averages."
        elif short_ma > long_ma:
            trend = "The short-term trend is potentially bullish, with the short-term moving average above the long-term moving average."
        else:
            trend = "The short-term trend is potentially bearish, with the short-term moving average below the long-term moving average."
        
        if adx > 25:
            if di_plus > di_minus:
                trend += " The trend is strong and bullish according to ADX."
            else:
                trend += " The trend is strong and bearish according to ADX."
        else:
            trend += " The trend is weak according to ADX."
        
        return trend

    def _analyze_weekly_trend(self, prices: List[float], adx: float, di_plus: float, di_minus: float) -> str:
        weekly_returns = [(prices[i] - prices[i-7])/prices[i-7] for i in range(7, len(prices), 7)]
        avg_weekly_return = np.mean(weekly_returns)
        
        trend = ""
        if avg_weekly_return > 0.05:
            trend = "The weekly trend is strongly bullish, with an average weekly return above 5%."
        elif avg_weekly_return > 0.02:
            trend = "The weekly trend is moderately bullish, with an average weekly return between 2% and 5%."
        elif avg_weekly_return > 0:
            trend = "The weekly trend is slightly bullish, with a positive average weekly return."
        elif avg_weekly_return > -0.02:
            trend = "The weekly trend is slightly bearish, with a small negative average weekly return."
        elif avg_weekly_return > -0.05:
            trend = "The weekly trend is moderately bearish, with an average weekly return between -2% and -5%."
        else:
            trend = "The weekly trend is strongly bearish, with an average weekly return below -5%."
        
        if adx > 25:
            if di_plus > di_minus:
                trend += " The trend is strong and bullish according to ADX."
            else:
                trend += " The trend is strong and bearish according to ADX."
        else:
            trend += " The trend is weak according to ADX."
        
        return trend

    def _analyze_monthly_trend(self, prices: List[float], adx: float, di_plus: float, di_minus: float) -> str:
        monthly_returns = [(prices[i] - prices[i-30])/prices[i-30] for i in range(30, len(prices), 30)]
        avg_monthly_return = np.mean(monthly_returns)
        
        trend = ""
        if avg_monthly_return > 0.15:
            trend = "The monthly trend is strongly bullish, with an average monthly return above 15%."
        elif avg_monthly_return > 0.07:
            trend = "The monthly trend is moderately bullish, with an average monthly return between 7% and 15%."
        elif avg_monthly_return > 0:
            trend = "The monthly trend is slightly bullish, with a positive average monthly return."
        elif avg_monthly_return > -0.07:
            trend = "The monthly trend is slightly bearish, with a small negative average monthly return."
        elif avg_monthly_return > -0.15:
            trend = "The monthly trend is moderately bearish, with an average monthly return between -7% and -15%."
        else:
            trend = "The monthly trend is strongly bearish, with an average monthly return below -15%."
        
        if adx > 25:
            if di_plus > di_minus:
                trend += " The trend is strong and bullish according to ADX."
            else:
                trend += " The trend is strong and bearish according to ADX."
        else:
            trend += " The trend is weak according to ADX."
        
        return trend

    def _calculate_volume_change(self, volumes: List[float], period: int) -> float:
        if len(volumes) < period + 1:
            return 0
        current_volume = volumes[-1]
        previous_volume = volumes[-period-1]
        return ((current_volume - previous_volume) / previous_volume) * 100

    def _identify_divergence(self, prices: List[float], indicator: List[float], period: int) -> str:
        if len(prices) < period + 1 or len(indicator) < period + 1:
            return "Insufficient data for divergence analysis"
        price_change = prices[-1] - prices[-period-1]
        indicator_change = indicator[-1] - indicator[-period-1]
        if price_change > 0 and indicator_change < 0:
            return "Bearish divergence detected"
        elif price_change < 0 and indicator_change > 0:
            return "Bullish divergence detected"
        else:
            return "No divergence detected"

    def _calculate_mfi(self, prices: List[float], volumes: List[float], period: int) -> float:
        if len(prices) < period + 1 or len(volumes) < period + 1:
            return 50  # Return neutral MFI if insufficient data
        typical_prices = [(prices[i] + prices[i-1] + prices[i-2]) / 3 for i in range(2, len(prices))]
        raw_money_flow = [tp * volumes[i+2] for i, tp in enumerate(typical_prices)]
        positive_flow = sum(mf for mf, tp, prev_tp in zip(raw_money_flow[-period:], typical_prices[-period:], typical_prices[-period-1:]) if tp > prev_tp)
        negative_flow = sum(mf for mf, tp, prev_tp in zip(raw_money_flow[-period:], typical_prices[-period:], typical_prices[-period-1:]) if tp < prev_tp)
        if negative_flow == 0:
            return 100
        mfi = 100 - (100 / (1 + positive_flow / negative_flow))
        return mfi

    def _generate_recommendation(self, buy_signals, sell_signals, suggested_buy_price, suggested_sell_price,
                                 buy_reason, sell_reason, price, timeframe, support, resistance, 
                                 trend_analysis, profit_target, profit_reason, stop_loss, stop_loss_reason,
                                 volume_change, rsi_divergence, macd_divergence, mfi):
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
        recommendation += f"Stop loss: ${stop_loss:.2f}\n"
        recommendation += f"Stop loss reason: {stop_loss_reason}\n"
        
        recommendation += f"\nSell consideration:\n"
        recommendation += f"Suggested sell near: ${suggested_sell_price:.2f}\n"
        recommendation += f"Reason: {sell_reason}\n"

        recommendation += f"\nAdditional Indicators:\n"
        recommendation += f"Volume Change: {volume_change:.2f}%\n"
        recommendation += f"RSI Divergence: {rsi_divergence}\n"
        recommendation += f"MACD Divergence: {macd_divergence}\n"
        recommendation += f"Money Flow Index: {mfi:.2f}\n"

        return recommendation