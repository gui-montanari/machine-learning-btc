from typing import Dict, Any, Optional
from .data_fetcher import DataFetcher
from .indicators import Indicators
from .recommendation_engine import RecommendationEngine
import logging

class BitcoinAnalyzer:
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.indicators = Indicators()
        self.recommendation_engine = RecommendationEngine()

    def run_analysis(self) -> Optional[Dict[str, Any]]:
        real_time_price = self.data_fetcher.fetch_real_time_price()
        if not real_time_price:
            logging.error("Failed to fetch real-time price. Aborting analysis.")
            return None

        if not self.data_fetcher.fetch_historical_data():
            logging.error("Failed to fetch historical data. Aborting analysis.")
            return None

        self.indicators.set_data(self.data_fetcher.prices, self.data_fetcher.volumes)

        # Calculate indicators
        analysis_results = self._calculate_indicators(real_time_price)

        # Get recommendations
        analysis_results.update(self._get_recommendations(analysis_results))

        return analysis_results

    def _calculate_indicators(self, real_time_price: float) -> Dict[str, Any]:
        return {
            'real_time_price': real_time_price,
            'opening_price': self.data_fetcher.prices[-1],
            'volume_ma': self.indicators.calculate_volume_ma(),
            'volatility': self.indicators.calculate_volatility(),
            'rsi': self.indicators.calculate_rsi(),
            'percentage_change': self.indicators.calculate_percentage_change(),
            'predicted_price': self.indicators.calculate_linear_regression(),
            'bollinger_bands': self.indicators.calculate_bollinger_bands(),
            'ema': self.indicators.calculate_ema(),
            'fib_levels': self.indicators.calculate_fibonacci_levels(),
            'macd': self.indicators.calculate_macd(),
            'adx': self.indicators.calculate_adx(),
            'stochastic': self.indicators.calculate_stochastic(),
            'ichimoku_cloud': self.indicators.calculate_ichimoku_cloud(),
            'pivot_points': self.indicators.calculate_pivot_points(),
            'high_price': self.data_fetcher.high_price,
            'low_price': self.data_fetcher.low_price,
            'last_timestamp': self.data_fetcher.dates[-1],
            'prices': self.data_fetcher.prices,
            'volumes': self.data_fetcher.volumes
        }

    def _get_recommendations(self, data: Dict[str, Any]) -> Dict[str, str]:
        recommendations = {}
        for timeframe in ['real-time', 'daily', 'weekly', 'monthly']:
            recommendations[f'{timeframe}_recommendation'] = self.recommendation_engine.get_recommendation(
                data['opening_price'], data['rsi'], *data['macd'], data['fib_levels'],
                *data['ichimoku_cloud'][2:4], data['ema'], *data['adx'], data['stochastic'],
                *data['bollinger_bands'], timeframe, data['prices'], data['volumes'], data['pivot_points']
            )
        return recommendations