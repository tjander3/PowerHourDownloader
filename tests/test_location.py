import pytest

from powerhourdownloader.location import Location

class TestLocation:

    @pytest.mark.parametrize(
            'kwargs, expected_results', (
                ({'x': 3, 'y': 4}, (3, 4)),
                ({'x': 3, 'y': 4, 'str_loc': 'center'}, (3, 4)),
                ({'str_loc': 'center'}, 'center'),
            )
        )
    def test_location(self, kwargs, expected_results):
        loc = Location(**kwargs)
        assert loc.location == expected_results
