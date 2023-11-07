from pathlib import Path
import pytest
from powerhourdownloader.location import Location
from powerhourdownloader.text_video_overlay import TextVideoOverlay

from powerhourdownloader.transition_video import TransitionVideo

class TestTransitionVideo:

    # TODO finish implementing this need to write file and actually compare and make a short video to actually compare
    @pytest.mark.parametrize(
            'video_path, text, location, expected_result',
            (
                (
                    Path(__file__).parent / 'videos' / 'test_video.mp4',
                    'Hello there',
                    Location(str_loc='top left'),
                    Path(__file__).parent / 'videos' / 'test_video_hello_there.mp4',
                ),
            )
    )
    def test_transition_video(
        self,
        video_path: Path,
        text: str,
        location: Location,
        expected_result: Path,
    ) -> None:
        # TODO left off here
        # TODO do a golden test here with parmatrie, will ave to add video to git repo thugh
        text_overlay = TextVideoOverlay(text=text, text_color=None, text_location=location)
        transition_video = TransitionVideo(video=video_path, text=text_overlay, audio=None)
