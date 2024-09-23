class AnalysisPrinter:
    @staticmethod
    def format_analysis_results(results):
        formatted_text = "Bitcoin Analysis Results\n"
        formatted_text += "=" * 30 + "\n\n"
        
        formatted_text += f"Real-time BTC Price (USD): ${results['real_time_price']:.2f}\n"
        formatted_text += f"Opening BTC Price (USD): ${results['opening_price']:.2f}\n"
        formatted_text += f"Daily High (USD): ${results['high_price']:.2f}\n"
        formatted_text += f"Daily Low (USD): ${results['low_price']:.2f}\n"
        formatted_text += f"Predicted BTC Price (USD): ${results['predicted_price']:.2f}\n"
        formatted_text += f"Last data timestamp: {results['last_timestamp']} Sao Paulo UTC -3\n\n"
        
        formatted_text += f"Volume MA (8 days, USD): ${results['volume_ma'][-1]:.2f}b\n"
        formatted_text += f"Percentage Change (8 days): {results['percentage_change']:.2f}%\n"
        formatted_text += f"Volatility: {results['volatility']:.2f}\n"
        formatted_text += f"RSI (14 periods): {results['rsi'][-1]:.2f}\n"
        formatted_text += f"EMA (8 periods, USD): ${results['ema'][-1]:.2f}\n"
        formatted_text += f"Lower Bollinger Band (USD): ${results['bollinger_bands'][1]:.2f}\n"
        formatted_text += f"Upper Bollinger Band (USD): ${results['bollinger_bands'][0]:.2f}\n"
        formatted_text += f"ADX: {results['adx'][0]:.2f}\n"
        formatted_text += f"DI+: {results['adx'][1]:.2f}\n"
        formatted_text += f"DI-: {results['adx'][2]:.2f}\n\n"
        
        formatted_text += "Fibonacci Levels (USD):\n"
        for i, level in enumerate([23.6, 38.2, 61.8]):
            formatted_text += f"{level}% : ${results['fib_levels'][i]:.2f}\n"
        
        formatted_text += "\nIchimoku Cloud:\n"
        formatted_text += f"Support (Senkou Span A): ${results['ichimoku_cloud'][2]:.2f}\n"
        formatted_text += f"Resistance (Senkou Span B): ${results['ichimoku_cloud'][3]:.2f}\n"
        
        trend = 'Bullish' if results['real_time_price'] > results['ichimoku_cloud'][3] else 'Bearish' if results['real_time_price'] < results['ichimoku_cloud'][2] else 'Neutral'
        formatted_text += f"Current Trend: {trend}\n\n"
        
        formatted_text += "Pivot Points:\n"
        pivot_names = ['Pivot', 'R1', 'S1', 'R2', 'S2', 'R3', 'S3']
        for name, value in zip(pivot_names, results['pivot_points']):
            formatted_text += f"{name}: ${value:.2f}\n"
        
        for timeframe in ['real-time', 'daily', 'weekly', 'monthly']:
            formatted_text += f"\n{timeframe.capitalize()} Recommendation:\n"
            formatted_text += f"{results[f'{timeframe}_recommendation']}\n"
        
        return formatted_text
