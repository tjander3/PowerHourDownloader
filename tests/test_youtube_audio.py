import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from powerhourdownloader.youtube_audio import YoutubeAudio
from powerhourdownloader.youtube_video import YoutubeVideo, main
from powerhourdownloader.video_link import VideoLink
from tests.helper_functions_for_tests import compare_file_sizes


class TestYoutubeVideo:
    @pytest.fixture
    def youtube_audio(self):
        """Fixture for a YoutubeVideo object."""
        return YoutubeAudio(
            video_link=VideoLink(video_link='https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            name='Rick Astley - Never Gonna Give You Up',
            video=None,
            start_time=0,
            end_time=10,
        )

    def test_youtube_video_init(self, youtube_audio):
        """Test initialization of YoutubeVideo."""
        assert youtube_audio.video_link.video_link == 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        assert youtube_audio.name == 'Rick Astley - Never Gonna Give You Up'
        assert youtube_audio.video is None
        assert youtube_audio.start_time == 0
        assert youtube_audio.end_time == 10

    def test_download(self, youtube_audio: YoutubeAudio):
        """Test downloading a YouTube video."""
        youtube_audio.download()
        video_path = Path(youtube_audio.video)
        print(video_path)
        assert video_path.exists()
        pre_downloaded_video = Path(__file__).parent / 'videos' / 'Rick Astley - Never Gonna Give You Up.mp3'
        assert compare_file_sizes(video_path, pre_downloaded_video, tolerance=0.1)
        # TODO add a function to compare to make sure every bit is equal
