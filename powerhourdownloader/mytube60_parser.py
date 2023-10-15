from powerhourdownloader.power_hour_parser import PowerHourParser


class MyTube60Parser(PowerHourParser):
    def __init__(self) -> None:
        raise NotImplementedError

    def parse(self):
        raise NotImplementedError
