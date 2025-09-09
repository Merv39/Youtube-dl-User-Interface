# tests/test_downloader_mocked.py
import unittest
from unittest.mock import patch, MagicMock
from yt_dl_gui.downloader import download_video

class TestYoutubeDownloaderMocked(unittest.TestCase):

    @patch("yt_dl_gui.downloader.YoutubeDL")
    def test_valid_youtube_URL(self, mock_ydl_class):
        mock_ydl = MagicMock()
        # No exception raised
        mock_ydl.download.return_value = None
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        result = download_video("https://www.youtube.com/watch?v=valid", "mp3")
        self.assertTrue(result)

    @patch("yt_dl_gui.downloader.YoutubeDL")
    def test_invalid_youtube_URL(self, mock_ydl_class):
        mock_ydl = MagicMock()
        # Simulate a download failure
        mock_ydl.download.side_effect = Exception("Invalid URL")
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        result = download_video("https://www.google.com", "mp3")
        self.assertFalse(result)

    @patch("yt_dl_gui.downloader.YoutubeDL")
    def test_unavailable_youtube_URL(self, mock_ydl_class):
        mock_ydl = MagicMock()
        # Simulate a download failure
        mock_ydl.download.side_effect = Exception("Invalid URL")
        mock_ydl_class.return_value.__enter__.return_value = mock_ydl

        result = download_video("https://www.youtube.com/watch?v=test", "mp3")
        self.assertFalse(result)


# To run type into the project folder:
# python -m unittest -v tests.test_downloader_real