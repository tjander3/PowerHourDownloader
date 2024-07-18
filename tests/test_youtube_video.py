import os
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from powerhourdownloader.youtube_video import YoutubeVideo, main
from powerhourdownloader.video_link import VideoLink


def get_file_size(file_path):
    return os.path.getsize(file_path)


def compare_file_sizes(video1_path, video2_path, tolerance=0.01):
    size1 = get_file_size(video1_path)
    size2 = get_file_size(video2_path)

    size_diff = abs(size1 - size2)
    avg_size = (size1 + size2) / 2

    percentage_diff = size_diff / avg_size

    if percentage_diff <= tolerance:
        print("File sizes are within 1% of each other.")
        return True
    else:
        print(f"File sizes differ by more than 1%: {percentage_diff * 100:.2f}%")
        return False


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
