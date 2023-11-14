from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from powerhourdownloader.video import Video

from powerhourdownloader.video_link import VideoLink


@dataclass
class YoutubeVideo(Video):
    video_link: VideoLink
    name: str
    video: Optional[Path]
    start_time: Optional[float]
    end_time: Optional[float]

    def download(self) -> Path:
        raise NotImplementedError
