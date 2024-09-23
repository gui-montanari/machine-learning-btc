import sys
from PyQt5.QtWidgets import QApplication
from src.gui.bitcoin_analyzer_gui import BitcoinAnalyzerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BitcoinAnalyzerGUI()
    window.show()
    sys.exit(app.exec_())