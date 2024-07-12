import pytest
from powerhourdownloader.power_hour import PowerHour, DownloadStatusEnum
from powerhourdownloader.video import Video
from powerhourdownloader.transition import Transition
from pathlib import Path
from unittest.mock import MagicMock, patch

class MockVideo(Video):
    def __init__(self, name, video=None, video_link=None, start_time=None, end_time=None):
        super().__init__(name=name, video=video, video_link=video_link, start_time=start_time, end_time=end_time)

    def download(self) -> None:
        # Do nothing
        pass
        # 2. Mock the download behavior (if you need to test specific download scenarios)
        #    For example:
        #    self.video = Path("path/to/mock/video.mp4")

class MockTransition(Transition):
    def __init__(self, video=None, text=None, audio=None, output=None):
        super().__init__(video=video, text=text, audio=audio, output=output)

@pytest.fixture
def power_hour():
    """Fixture for a PowerHour object."""
    videos = [MockVideo(f"Video {i}", video_link="https://www.youtube.com/watch?v=dQw4w9WgXcQ", start_time=0, end_time=10) for i in range(3)]
    transitions = [MockTransition(video=Path("path/to/mock/video.mp4")) for _ in range(3)]
    return PowerHour(videos=videos, transitions=transitions)

class TestPowerHour:
    def test_power_hour_init(self, power_hour):
        """Test initialization of PowerHour."""
        assert power_hour.videos_downloaded == 0
        assert power_hour.power_hour_status == DownloadStatusEnum.WAITING
        assert power_hour.total_videos is None

    def test_power_hour_set_transitions(self, power_hour):
        """Test setting transitions."""
        # Test with None
        power_hour.transitions = None
        assert power_hour.transitions == None
        power_hour._set_transitions()
        assert power_hour.transitions == [None for _ in range(3)]

        # Test with single transition
        transition = MockTransition()
        power_hour.transitions = transition
        assert power_hour.transitions == transition
        power_hour._set_transitions()
        assert power_hour.transitions == [transition for _ in range(3)]

        # Test with list of transitions
        transitions = [MockTransition(), None, MockTransition()]
        power_hour.transitions = transitions
        assert power_hour.transitions == transitions
        power_hour._set_transitions()
        assert power_hour.transitions == transitions

    # TODO left off here
    @pytest.mark.skip
    def test_power_hour_combine_videos(self, power_hour, monkeypatch):
        """Test combining videos."""
        # Mock concatenate_videoclips
        mock_concatenate = MagicMock()
        monkeypatch.setattr("moviepy.editor.concatenate_videoclips", mock_concatenate)

        # Mock VideoFileClip
        mock_videofileclip = MagicMock()
        monkeypatch.setattr("moviepy.editor.VideoFileClip", mock_videofileclip)

        # Mock write_videofile
        mock_write_videofile = MagicMock()
        mock_videofileclip.return_value.write_videofile = mock_write_videofile

        power_hour.combine_videos()

        # Assert status is updated
        assert power_hour.power_hour_status == DownloadStatusEnum.VIDEOS_COMBINING

        # Assert concatenate_videoclips is called
        mock_concatenate.assert_called_once()

        # Assert write_videofile is called
        mock_write_videofile.assert_called_once()

    def test_power_hour_create_power_hour(self, power_hour, monkeypatch):
        """Test creating power hour."""
        # Mock download method
        mock_download = MagicMock()
        for video in power_hour.videos:
            monkeypatch.setattr(video, "download", mock_download)

        # Mock combine_videos
        mock_combine_videos = MagicMock()
        monkeypatch.setattr(power_hour, "combine_videos", mock_combine_videos)

        power_hour.create_power_hour()

        # Assert status is updated
        assert power_hour.power_hour_status == DownloadStatusEnum.VIDEOS_DONE

        # Assert download is called for each video
        assert mock_download.call_count == 3

        # Assert combine_videos is called
        mock_combine_videos.assert_called_once()

    # TODO left off here
    @pytest.mark.skip
    def test_power_hour_create_power_hour_failed(self, power_hour, monkeypatch):
        """Test creating power hour with failed download."""
        # Mock download method to raise an exception
        mock_download = MagicMock(side_effect=Exception("Download failed"))
        for video in power_hour.videos:
            monkeypatch.setattr(video, "download", mock_download)

        # Mock combine_videos
        mock_combine_videos = MagicMock()
        monkeypatch.setattr(power_hour, "combine_videos", mock_combine_videos)

        try:
            power_hour.create_power_hour()
        except Exception:
            # Assert status is updated to FAILED
            assert power_hour.power_hour_status == DownloadStatusEnum.FAILED

            # Assert combine_videos is not called
            mock_combine_videos.assert_not_called()

    def test_power_hour_save_power_hour(self, power_hour):
        """Test saving power hour."""
        # This test is not implemented as save_power_hour is not defined in the code.
        # You would need to implement the save_power_hour method in the PowerHour class
        # and then write the test accordingly.
        pass

    def test_power_hour_upload_power_hour(self, power_hour):
        """Test uploading power hour."""
        # This test is not implemented as upload_power_hour is not defined in the code.
        # You would need to implement the upload_power_hour method in the PowerHour class
        # and then write the test accordingly.
        pass
