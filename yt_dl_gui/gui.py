from PyQt5.QtWidgets import QMainWindow, QLineEdit, QVBoxLayout, QPushButton, QWidget, QPlainTextEdit
from PyQt5.QtCore import QObject, pyqtSignal
from downloader import download_video
import sys

class EmittingStream(QObject):
    text_written = pyqtSignal(str)

    def write(self, text):
        if text.strip():
            self.text_written.emit(text)
    
    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 200)

        # -- Widgets --
        
        self.e1 = QLineEdit(self)
        self.e1.setPlaceholderText("Enter video URL here")

        e2 = QPushButton("Download", self)
        e2.clicked.connect(self.handle_download)

        self.terminal = QPlainTextEdit(self)
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("background-color: black; color: lime; font-family: monospace;")
        self.terminal.setLineWrapMode(QPlainTextEdit.NoWrap)
    
        # -- Layout --

        vbox = QVBoxLayout()
        vbox.addWidget(self.e1)
        vbox.addWidget(e2)
        vbox.addWidget(self.terminal)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.setWindowTitle("YouTube Downloader")
    
        # Redirect stdout to the terminal widget
        self.stdout_stream = EmittingStream()
        self.stdout_stream.text_written.connect(self.append_output)
        sys.stdout = self.stdout_stream

    def append_output(self, text: str) -> None:
        self.terminal.appendPlainText(text)

    def handle_download(self):
        url = self.e1.text()
        download_video(url)