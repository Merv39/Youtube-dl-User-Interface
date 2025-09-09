from PyQt5.QtWidgets import QMainWindow, QLineEdit, QVBoxLayout, QPushButton, QWidget, QPlainTextEdit, QComboBox, QHBoxLayout
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from downloader import download_video, download_dir
import sys
import subprocess
import os
import re

class DownloadWorker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)

    def __init__(self, url: str, format_type = None):
        super().__init__()
        self.url = url
        self.format_type = format_type
        self._stop_flag = False
    
    def run(self):
        download_video(self.url, self.format_type, get_stop_flag=self.get_stop_flag)
        self.finished.emit()
    
    def set_stop_flag(self, b : bool):
        self._stop_flag = b
    
    def get_stop_flag(self) -> bool:
        return self._stop_flag

"""
This class is used to move the terminal output to an output on the GUI
"""
class EmittingStream(QObject):
    text_written = pyqtSignal(str)
    def ansi_escape(self, text):
        return re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]').sub('', text)

    def write(self, text):
        if text.strip():
            self.text_written.emit(self.ansi_escape(text))
    
    def flush(self):
        pass

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 200)

        # -- Widgets --
        
        self.e1 = QLineEdit(self)
        self.e1.setPlaceholderText("Enter video URL here")
        self.e1.returnPressed.connect(self.handle_download)

        e2 = QPushButton("Download", self)
        e2.clicked.connect(self.handle_download)
        e3 = QPushButton("Abort", self)
        e3.clicked.connect(self.handle_abort)

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

        # Open Downloads Folder button
        self.open_folder_btn = QPushButton("Open Downloads Folder", self)
        self.open_folder_btn.clicked.connect(self.open_downloads_folder)
    
        # -- Layout --

        # Create horizontal layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(e2)
        button_layout.addWidget(e3)
        button_layout.addWidget(self.open_folder_btn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.e1)
        vbox.addWidget(self.dropdown)
        vbox.addLayout(button_layout)
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

    def open_downloads_folder(self):
        """Open the downloads folder in Windows Explorer"""
        try:
            # Use the downloads directory from downloader.py
            # Ensure the directory exists (it should already exist from downloader.py)
            os.makedirs(download_dir, exist_ok=True)
            
            # Open in Windows Explorer (explorer often returns non-zero even on success)
            subprocess.run(['explorer', download_dir], check=False)
            print(f"Opened downloads folder: {download_dir}")
            
        except Exception as e:
            print(f"Error opening downloads folder: {e}")

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
    
    def handle_abort(self):
        print("Aborting download.")
        self.worker.set_stop_flag(True)