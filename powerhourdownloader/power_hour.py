from dataclasses import dataclass
from pathlib import Path

from powerhourdownloader.video import Video
from powerhourdownloader.transition import Transition


@dataclass
class PowerHour:
    videos: list[Video]
    transitions: list[Transition]

    def create_power_hour(self) -> Path:
        raise NotImplementedError

    def save_power_hour(self) -> Path:
        raise NotImplementedError

    def upload_power_hour(self) -> None:
        raise NotImplementedError