import hashlib
from pathlib import Path
import pytest

from powerhourdownloader.location import Location
from powerhourdownloader.text_video_overlay import TextVideoOverlay
from powerhourdownloader.transition_image import TransitionImage

pytest.mark.xfail
class TestTransitionImage:
    @pytest.mark.parametrize(
            'image_path, text, location, expected_result',
            (
                (
                    Path(__file__).parent / 'images' / 'rory.jpg',
                    'Hello there',
                    Location(str_loc=('left', 'top')),
                    Path(__file__).parent / 'videos' / 'golden-transition-image-top-left.mp4',
                ),
            )
            # TODO test x y cord
    )
    def test_transition_image(
        self,
        image_path: Path,
        text: str,
        location: Location,
        expected_result: Path,
        tmp_path: Path,
    ) -> None:
        # TODO how much space is being used here?
        text_overlay = TextVideoOverlay(text=text, text_location=location)
        transition_video = TransitionImage(video=image_path, output=tmp_path, text=text_overlay, audio=None)

        transition_video_hash = open(transition_video.video, 'rb').read()
        golden_video_hash = open(expected_result, 'rb').read()

        assert (
            hashlib.sha512(transition_video_hash).hexdigest()
            == hashlib.sha512(golden_video_hash).hexdigest())
