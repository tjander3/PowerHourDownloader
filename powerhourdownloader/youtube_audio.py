from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Optional

import yt_dlp as youtube_dl
from moviepy.editor import VideoFileClip

from powerhourdownloader.video import Video, txt2filename
from powerhourdownloader.video_link import VideoLink
from powerhourdownloader.youtube_video import YoutubeVideo


@dataclass
class YoutubeAudio(YoutubeVideo):

    def __post_init__(self):
        super().__post_init__()
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'overwrites': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    def download(self, audio_only=True) -> None:
        """Download youtube video.
        Args:
            audio_only (bool, optional): Only use audio. Defaults to False.

        Returns:
            None: This does not return anything but the video downloaded should be
                in the location stored in self.video
        """
        logging.debug("Starting to download audio")
        super().download(audio_only=True)

def main():
    # TODO need to test this
    youtube_video = YoutubeAudio(
        video_link=VideoLink(video_link='https://www.youtube.com/watch?v=ap0mqwvf7H0'),
        name='Taking Back Sunday - Cute Without the \\"E\\" (Cut From the Team)',
        video=None,
        start_time=2,
        end_time=20,
    )

    youtube_video.download()


if __name__ == '__main__':
    main()
