from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from powerhourdownloader.video_link import VideoLink


@dataclass
class Video(ABC):
    video_link: VideoLink
    name: str
    video: Optional[Path]
    start_time: Optional[float]
    end_time: Optional[float]

    @abstractmethod
    def download(self) -> Path:
        raise NotImplementedError
