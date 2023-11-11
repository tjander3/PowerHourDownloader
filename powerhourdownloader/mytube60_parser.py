from dataclasses import dataclass, field
from pathlib import Path
from powerhourdownloader.power_hour import PowerHour
from powerhourdownloader.power_hour_parser import PowerHourParser


@dataclass
class MyTube60Parser(PowerHourParser):
    link: str
    power_hour: PowerHour = field(init=False)

    def _get_webpage(self):
        """Get powerhour webpage from self.link"""
        # TODO left off here
        raise NotImplementedError

    def parse(self):
        videos = []
        powerhour_webpage = self._get_webpage()
        raise NotImplementedError


def main():
    link = 'https://www.mytube60.com/video/on/emo-night/b664367fb7ee40799dccbe693015d6f6.html'

    mytube60 = MyTube60Parser(link=link)
    mytube60.parse()


if __name__ == '__main__':
    main()
