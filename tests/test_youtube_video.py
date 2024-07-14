import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from powerhourdownloader.youtube_video import YoutubeVideo, main
from powerhourdownloader.video_link import VideoLink

class TestYoutubeVideo:
    @pytest.fixture
    def youtube_video(self):
        """Fixture for a YoutubeVideo object."""
        return YoutubeVideo(
            video_link=VideoLink(video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            name='Rick Astley - Never Gonna Give You Up',
            video=None,
            start_time=0,
            end_time=10,
        )

    def test_youtube_video_init(self, youtube_video):
        """Test initialization of YoutubeVideo."""
        assert youtube_video.video_link.video_link == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        assert youtube_video.name == 'Rick Astley - Never Gonna Give You Up'
        assert youtube_video.video is None
        assert youtube_video.start_time == 0
        assert youtube_video.end_time == 10

    #@patch('powerhourdownloader.youtube_video.youtube_dl.YoutubeDL')
    def test_download(self, youtube_video):
        """Test downloading a YouTube video."""
        youtube_video.download()
        assert youtube_video.name.exists()
        print(youtube_video.name)
        print(type(youtube_video))
        assert False
