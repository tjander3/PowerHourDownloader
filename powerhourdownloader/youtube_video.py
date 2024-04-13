from dataclasses import dataclass
import logging
from pathlib import Path
from typing import Optional

import youtube_dl
from moviepy.editor import VideoFileClip

from powerhourdownloader.video import Video, txt2filename
from powerhourdownloader.video_link import VideoLink
from powerhourdownloader.debug_variables import target_resolution


@dataclass
class YoutubeVideo(Video):

    def __post_init__(self):
        self.ydl_opts = {'format': 'bestvideo+bestaudio/best', 'overwrites': True, 'retries': 25}
        if self.name is None:
            with youtube_dl.YoutubeDL() as ydl:
                  info_dict = ydl.extract_info(self.video_link.video_link, download=False)
                  # Misc info you can get, keeping around incase we need it
                  # video_url = info_dict.get("url", None)
                  # video_id = info_dict.get("id", None)
                  video_title = info_dict.get('title', None)
                  self.name = video_title

    def download(self, audio_only=False) -> None:
        """Download youtube video.
        Args:
            audio_only (bool, optional): Only use audio. Defaults to False.

        Returns:
            None: This does not return anything but the video downloaded should be
                in the location stored in self.video
        """
        logging.debug("Starting to download video")
        if self.video is None:
            # This will set self.video and make sure the directory exists
            self.setup_download_dir(audio_only=audio_only)


        if audio_only is True:
            file_extension = 'mp3'
        else:
            file_extension = 'mp4'

        full_video_path = self.video.parent / f'{txt2filename(self.name)}-full-video.{file_extension}'
        # add to download parameters:
        self.ydl_opts['outtmpl'] = str(full_video_path)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.video_link.video_link])

        # extract the relevant subclip:
        if self.start_time is not None:
            from moviepy.audio.io.AudioFileClip import AudioFileClip
            if audio_only == True:  # TODO can I check the class instead?
                with AudioFileClip(str(full_video_path)) as audio:
                    subclip = audio.subclip(self.start_time, self.end_time)
                    subclip.write_audiofile(str(self.video))

            else:
                with VideoFileClip(str(full_video_path), target_resolution=target_resolution) as video:
                    subclip = video.subclip(self.start_time, self.end_time)
                    subclip.write_videofile(str(self.video))
        else:
            # Have to rename file since we use fill_video_path
            if self.video.exists():
                self.video.unlink()
            full_video_path.rename(self.video)

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
