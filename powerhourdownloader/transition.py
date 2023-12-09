import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from moviepy.editor import (AudioFileClip, CompositeAudioClip,
                            CompositeVideoClip, TextClip, VideoFileClip)

from powerhourdownloader.text_video_overlay import TextVideoOverlay


@dataclass
class Transition():
    video: Path
    text: TextVideoOverlay = None
    audio: str = None  # TODO this needs to be an audio class
    output: Optional[Path] = None

    def _add_text_to_video(self) -> None:
        # TODO this should be in post init
        # TODO this could be in the parent class
        # Python program to write
        # text on video
        if self.text is None:
            # If there is no text to add do not do anything
            return

        logging.debug(self.video.absolute())
        if self.video.exists():
            logging.debug(f'video exist: {self.video.exists()}')
        else:
            logging.error(f'video does not exist: {self.video.exists()}')

        video = VideoFileClip(str(self.video))

        # Make the text. Many more options are available.
        txt_clip = (
            TextClip(self.text.text, fontsize=70, color=self.text.text_color)
                .set_position(self.text.text_location.location)
                .set_duration(video.duration)
        )

        result = CompositeVideoClip([video, txt_clip])  # Overlay text on video
        # TODO find out original video fps?
        # TODO what name to use
        if self.output:
            self.updated_video = self.output / f'text-added-{self.video.name}'
        else:
            self.updated_video = self.video.parent / f'text-added-{self.video.name}'

        result.write_videofile(str(self.updated_video), fps=25)  # Many options...

    @abstractmethod
    def _add_audio_to_video(self) -> None:
        raise NotImplementedError
