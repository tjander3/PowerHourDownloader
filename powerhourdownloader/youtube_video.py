from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import youtube_dl
from moviepy.editor import VideoFileClip

from powerhourdownloader.video import Video
from powerhourdownloader.video_link import VideoLink


@dataclass
class YoutubeVideo(Video):
    def download(self) -> Path:
        # TODO rename / fix these
        full_video_path = 'full_video.mp4'
        input_clip_path = 'input_clip.mp4'
        # download parameters:
        ydl_opts = {'format': 'best', 'overwrites': True, 'outtmpl': full_video_path}
        #ydl_opts = {'outputmpl': full_video_path}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.video_link.video_link])

        # extract the relevant subclip:
        if self.start_time is not None:
            with VideoFileClip(full_video_path) as video:
                subclip = video.subclip(self.start_time, self.end_time)
                subclip.write_videofile(input_clip_path)

def main():
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
