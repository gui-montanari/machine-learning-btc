# Bitcoin Analyzer

## Description

Bitcoin Analyzer is a technical analysis tool for Bitcoin, providing buy/sell recommendations based on multiple technical indicators. The project offers analyses for both the current moment and the day, considering various market factors.

## Features

- Real-time analysis of Bitcoin price
- Calculation of multiple technical indicators (RSI, MACD, Bollinger Bands, etc.)
- Buy/sell recommendations with detailed justifications
- Suggested prices for buying and selling
- Short and medium-term trend analysis

## Requirements

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/seu-usuario/bitcoin-analyzer.git
   cd bitcoin-analyzer
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Execute the main script:

```
python main.py
```

The program will fetch updated Bitcoin data, perform the analysis, and display the results in the console.

## Project Structure

- `main.py`: Entry point of the program
- `bitcoin_analyzer.py`: Main analysis class
- `data_fetcher.py`: Responsible for fetching market data
- `indicators.py`: Calculations of technical indicators
- `requirements.txt`: List of project dependencies

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or report bugs.

## Disclaimer

This project is for educational and research purposes only. It is not investment advice. Always do your own research and consider consulting a financial professional before making any investment.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contact

For questions or suggestions, please open an issue on GitHub or contact through guilhermemontanari8@gmail.com.
