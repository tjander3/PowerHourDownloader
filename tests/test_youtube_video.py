import pytest

from powerhourdownloader.youtube_video import YoutubeVideo, main


pytest.mark.xfail
class TestYoutubeVideo:
    def test_youtube_video(self):
        raise NotImplementedError

    def test_download(self):
        raise NotImplementedError

    def test_main(self):
        # We just want to verify main runs without any errors
        main()
