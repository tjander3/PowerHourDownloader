from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Optional

import youtube_dl
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
        if self.video is None:
            # This will set self.video and make sure the directory exists
            self.setup_download_dir()

        full_video_path = self.video.parent / f'{txt2filename(self.name)}-full-video.mp4'
        # add to download parameters:
        self.ydl_opts['outtmpl'] = str(full_video_path)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.video_link.video_link])

        # extract the relevant subclip:
        if self.start_time is not None:
            with VideoFileClip(str(full_video_path)) as video:
                subclip = video.subclip(self.start_time, self.end_time)
                subclip.write_videofile(str(self.video))
        else:
            # Have to rename file since we use fill_video_path
            if self.video.exists():
                self.video.unlink()
            full_video_path.rename(self.video)

def main():
    # TODO need to test this
    youtube_video = YoutubeVideo(
        video_link=VideoLink(video_link='https://www.youtube.com/watch?v=ap0mqwvf7H0'),
        name='Taking Back Sunday - Cute Without the \\"E\\" (Cut From the Team)',
        video=None,
        start_time=2,
        end_time=3,
    )

    youtube_video.download()


if __name__ == '__main__':
    main()
