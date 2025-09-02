from PyQt5.QtWidgets import QMainWindow, QLineEdit, QVBoxLayout, QPushButton, QWidget
from downloader import download_video

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000, 200)

        self.e1 = QLineEdit(self)
        self.e1.setPlaceholderText("Enter video URL here")

        e2 = QPushButton("Download", self)
        e2.clicked.connect(self.handle_download)

        vbox = QVBoxLayout()
        vbox.addWidget(self.e1)
        vbox.addWidget(e2)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.setWindowTitle("YouTube Downloader")

    def handle_download(self):
        url = self.e1.text()
        download_video(url)