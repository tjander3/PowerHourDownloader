from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from powerhourdownloader.video import Video
from powerhourdownloader.transition import Transition


@dataclass
class PowerHour:
    videos: list[Video]
    transitions: Optional[list[Transition]]

    def create_power_hour(self) -> Path:
        # TODO left off here lets implemet this, baically loop over all videos and download.  could be good to use multiple cores for this as well
        # download youtube videos
        # stitch videos together
        for video, transition in zip(self.videos, self.transition):
            pass
        raise NotImplementedError

    def save_power_hour(self) -> Path:
        raise NotImplementedError

    def upload_power_hour(self) -> None:
        raise NotImplementedError
