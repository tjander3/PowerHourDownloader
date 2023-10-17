from abc import ABC, abstractmethod

from attr import dataclass
from powerhourdownloader.power_hour import PowerHour


@dataclass
class PowerHourParser(ABC):
    power_hour: PowerHour
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def parse(self) -> PowerHour:
        raise NotImplementedError
