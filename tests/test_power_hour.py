import pytest
from powerhourdownloader.power_hour import main

class TestPowerHour:
    def test_power_hour(self):
        raise NotImplementedError

    def test_create_power_hour(self):
        # TODO make sure that we test with 1 transition, list of transitions, and no transitions
        raise NotImplementedError

    def tets_save_power_hour(self):
        raise NotImplementedError

    def test_upload_power_hour(self):
        raise NotImplementedError

    def test_main(self):
        # TODO mark this as downloading youtube videos using pytest
        # We just want to verify main runs without any errors
        # Note this main function does reach out and download youtube vidoes
        main()
