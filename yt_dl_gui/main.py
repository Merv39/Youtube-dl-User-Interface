import sys
from PyQt5.QtWidgets import QApplication
try:
    from yt_dl_gui.gui import MainWindow    # for build execution
except ImportError:
    from gui import MainWindow              # for direct file execution

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())