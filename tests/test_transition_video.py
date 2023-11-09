import hashlib
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
                    Location(str_loc=('left', 'top')),
                    Path(__file__).parent / 'videos' / 'golden-transition-video-top-left.mp4',
                ),
            )
            # TODO test x y cord
    )
    def test_transition_video(
        self,
        video_path: Path,
        text: str,
        location: Location,
        expected_result: Path,
        tmp_path: Path,
    ) -> None:
        text_overlay = TextVideoOverlay(text=text, text_color=None, text_location=location)
        transition_video = TransitionVideo(video=video_path, output=tmp_path, text=text_overlay, audio=None)
        transition_video._add_text_to_video()  # TODO this should not be privagte

        transition_video_hash = open(transition_video.updated_video, 'rb').read()
        golden_video_hash = open(expected_result, 'rb').read()

        assert (
            hashlib.sha512(transition_video_hash).hexdigest()
            == hashlib.sha512(golden_video_hash).hexdigest())
