from PyQt5.QtWidgets import QMainWindow, QLineEdit, QVBoxLayout, QPushButton, QWidget, QPlainTextEdit, QComboBox
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from downloader import download_video
import sys

class DownloadWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def __init__(self, url: str, format_type = None):
        super().__init__()
        self.url = url
        self.format_type = format_type
    
    def run(self):
        download_video(self.url, self.format_type)
        self.finished.emit()

"""
This class is used to move the terminal output to an output on the GUI
"""
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
        self.terminal.setStyleSheet("""
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: monospace;
            font-size: 14px;
        """)
        self.terminal.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.dropdown = QComboBox()
        self.dropdown.addItems(['mp3', 'flac', 'mp4'])
    
        # -- Layout --

        vbox = QVBoxLayout()
        vbox.addWidget(self.e1)
        vbox.addWidget(self.dropdown)
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
        format_type = self.dropdown.currentText()
        self.thread = QThread()
        self.worker = DownloadWorker(url, format_type)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
        self.e1.setText("")