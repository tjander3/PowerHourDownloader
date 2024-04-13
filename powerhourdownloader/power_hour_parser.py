from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from powerhourdownloader.power_hour import PowerHour


@dataclass
class PowerHourParser(ABC):
    power_hour: PowerHour
    videos_verified: int = 0
    # Allow for special debugging during tests
    test_debug: Optional[str] = None

    @abstractmethod
    def parse(self) -> PowerHour:
        raise NotImplementedError
