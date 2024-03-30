import pytest
from powerhourdownloader.video_link import VideoLink, main

@pytest.mark.skip(reason="Youtube dl in ci problem")
class TestVideoLink:
    @pytest.mark.parametrize(
        'link, is_valid', (
            ('https://www.youtube.com/watch?v=mvVBuG4IOW4', True),
            ('https://www.youtube.com/watch?v=xxx', False),

        )
    )
    def test_verify_video_link(self, link, is_valid):
        assert VideoLink(link).verify_video_link() == is_valid

@pytest.mark.skip(reason="Youtube dl in ci problem")
def test_main():
    """Test main function in video_link.py

    Note ths function already has two asserts so just
    calling the function should be enough
    """
    main()
