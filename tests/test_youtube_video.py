import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from powerhourdownloader.youtube_video import YoutubeVideo, main
from powerhourdownloader.video_link import VideoLink
from tests.helper_functions_for_tests import compare_file_sizes, get_file_size


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

    def test_download(self, youtube_video: YoutubeVideo):
        """Test downloading a YouTube video."""
        youtube_video.download()
        video_path = Path(youtube_video.video)
        assert video_path.exists()
        pre_downloaded_video = Path(__file__).parent / 'videos' / 'Rick Astley - Never Gonna Give You Up.mp4'
        assert compare_file_sizes(video_path, pre_downloaded_video)
