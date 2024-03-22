import pytest

from powerhourdownloader.mytube60_parser import MyTube60Parser
from powerhourdownloader.power_hour_runner import PowerHourRunner

pytest.mark.xfail
class TestPowerHourRunner:
    def test_power_hour_runner(self):
        raise NotImplementedError

    def test_run(self):
        # TODO set debug values to make quicker
        audio_only = False
        webpage_link = 'https://www.mytube60.com/video/on/ttpmoose---movies/db30aa60461b4a3fa4375724b61b8013.html'

        mytube60 = MyTube60Parser(link=webpage_link)
        mytube60.parse(audio_only=audio_only)
        power_hour_runner = PowerHourRunner(parser=mytube60)
        power_hour_runner.run()

#def test_main():
#    raise NotImplementedError
