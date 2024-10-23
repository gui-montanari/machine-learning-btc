# src/gui/bitcoin_analyzer_gui.py
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QWidget, QPushButton, QTextEdit, QLabel, QFrame)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QIcon
from src.analyzer import BitcoinAnalyzer
from src.analysis_printer import AnalysisPrinter

class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)

class BitcoinAnalyzerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitcoin Analyzer")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #f0f0f0;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.setup_header()
        self.setup_content()
        self.setup_footer()

        self.analyzer = BitcoinAnalyzer()
        self.printer = AnalysisPrinter()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_price)
        self.timer.start(60000)  # Update every minute

    def setup_header(self):
        header = QFrame(self)
        header.setStyleSheet("background-color: #2C3E50; color: white; padding: 10px;")
        header_layout = QHBoxLayout(header)

        title_label = QLabel("Bitcoin Analyzer")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        header_layout.addWidget(title_label)

        self.price_label = QLabel("Current BTC Price: Loading...")
        self.price_label.setFont(QFont("Arial", 14))
        header_layout.addWidget(self.price_label, alignment=Qt.AlignRight)

        self.main_layout.addWidget(header)

    def setup_content(self):
        content_layout = QHBoxLayout()

        left_panel = QFrame(self)
        left_panel.setStyleSheet("background-color: #34495E; padding: 20px; border-radius: 10px;")
        left_layout = QVBoxLayout(left_panel)

        analyze_button = ModernButton("Analyze Bitcoin")
        analyze_button.clicked.connect(self.run_analysis)
        left_layout.addWidget(analyze_button)

        left_layout.addStretch()

        content_layout.addWidget(left_panel)

        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #bdc3c7;
                padding: 10px;
                border-radius: 5px;
                font-family: Courier;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        content_layout.addWidget(self.results_display, stretch=2)

        self.main_layout.addLayout(content_layout)

    def setup_footer(self):
        footer = QFrame(self)
        footer.setStyleSheet("background-color: #2C3E50; color: white; padding: 5px;")
        footer_layout = QHBoxLayout(footer)

        footer_text = QLabel("© 2024 Bitcoin Analyzer. All rights reserved.")
        footer_text.setFont(QFont("Arial", 10))
        footer_layout.addWidget(footer_text, alignment=Qt.AlignCenter)

        self.main_layout.addWidget(footer)

    def run_analysis(self):
        self.results_display.clear()
        self.results_display.append("Running analysis...")
        
        analysis_results = self.analyzer.run_analysis()
        
        if analysis_results:
            formatted_results = self.printer.format_analysis_results(analysis_results)
            self.results_display.setPlainText(formatted_results)
        else:
            self.results_display.append("Analysis failed. Please check the logs for more information.")

    def update_price(self):
        real_time_price = self.analyzer.data_fetcher.fetch_real_time_price()
        if real_time_price is not None:
            self.price_label.setText(f"Current BTC Price: ${real_time_price:.2f}")
        else:
            self.price_label.setText("Current BTC Price: Error fetching price")