from abc import ABC, abstractmethod
from powerhourdownloader.power_hour import PowerHour


class PowerHourParser(ABC):
    # TODO abstract
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def parse(self) -> PowerHour:
        raise NotImplementedError
