from dataclasses import dataclass
from pathlib import Path
from powerhourdownloader.power_hour import PowerHour
from powerhourdownloader.power_hour_parser import PowerHourParser


@dataclass
class MyTube60Parser(PowerHourParser):
    power_hour: PowerHour
    link: Path

    def parse(self):
        raise NotImplementedError
