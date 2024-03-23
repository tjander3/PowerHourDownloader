import pytest
from powerhourdownloader.video_link import VideoLink, main

class TestVideoLink:
    @pytest.mark.parametrize(
        'link, is_valid', (
            ('https://www.youtube.com/watch?v=mvVBuG4IOW4', True),
            ('https://www.youtube.com/watch?v=dpq4gmj-7ys', False),

        )
    )
    def test_verify_video_link(self, link, is_valid):
        assert VideoLink(link).verify_video_link() == is_valid

def test_main():
    """Test main function in video_link.py

    Note ths function already has two asserts so just
    calling the function should be enough
    """
    main()
