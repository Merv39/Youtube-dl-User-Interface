import unittest
from yt_dl_gui.downloader import download_video

class TestYoutubeDownloader(unittest.TestCase):
    def test_valid_youtube_URL(self):
        result = download_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "mp3")
        self.assertTrue(result)

    def test_invalid_youtube_URL(self):
        result = download_video("https://www.google.com", "mp3")
        self.assertFalse(result)

    def test_unavailable_youtube_url(self):
        result = download_video("https://www.youtube.com/watch?v=test", "mp3")
        self.assertFalse(result)


# To run type into the project folder:
# python -m unittest -v tests.test_download_real