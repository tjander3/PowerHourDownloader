from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from powerhourdownloader.video import Video

from powerhourdownloader.video_link import VideoLink


@dataclass
class YoutubeVideo(Video):
    def download(self) -> Path:
        raise NotImplementedError

def main():
    youtube_video = YoutubeVideo(
        video_link=VideoLink(video_link='https://www.youtube.com/watch?v=ap0mqwvf7H0'),
        name='Taking Back Sunday - Cute Without the \\"E\\" (Cut From the Team)',
        video=None,
        start_time=0,
        end_time=1,
    )

    youtube_video.download()


if __name__ == '__main__':
    main()
