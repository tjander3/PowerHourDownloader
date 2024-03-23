import pytest

from powerhourdownloader.text_video_overlay import TextVideoOverlay

class TestTextVideoOverlay:
    def test_init(self):
        text_overlay = TextVideoOverlay('Hello')
        assert text_overlay.text_location.location == 'center'

    # Use of this class is tested in test_transition and test_transition_video
