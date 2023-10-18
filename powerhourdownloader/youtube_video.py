from dataclasses import dataclass
from pathlib import Path
from powerhourdownloader.video import Video

from powerhourdownloader.video_link import VideoLink


@dataclass
class YoutubeVideo(Video):
    video_link: VideoLink
    video: Path

    def download(self, start_time=None, end_time=None) -> Path:
        raise NotImplementedError
