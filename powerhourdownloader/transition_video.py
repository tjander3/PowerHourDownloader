import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from moviepy.editor import (AudioFileClip, CompositeAudioClip,
                            CompositeVideoClip, TextClip, VideoFileClip)

from powerhourdownloader.location import Location
# TODO figure out why this is not importing
from powerhourdownloader.text_video_overlay import TextVideoOverlay
from powerhourdownloader.transition import Transition


@dataclass
class TransitionVideo(Transition):
    video: Path
    output: Optional[Path] = None
    updated_video: Path = field(init=False)
    text: Optional[TextVideoOverlay] = None
    audio: Optional[Path] = field(default=None)

    def __post_init__(self):
        if self.text is not None:
            self._add_text_to_video()
            # TODO deal with setting this
            self.video = self.updated_video

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


    def _add_audio_to_video(self) -> None:
        # TODO actually implement this
        videoclip = VideoFileClip("filename.mp4")
        audioclip = AudioFileClip("audioname.mp3")

        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile("new_filename.mp4")
        raise NotImplementedError

def main():
    tv = TransitionVideo(
        video=Path(__file__).parent / '..' / 'videos' / 'hello-there.mp4',
        text=TextVideoOverlay(text='Hello there', text_location=Location(str_loc=('left', 'top'))),
        audio=None,  # TODO this needs to be implemented still
    )

if __name__ == '__main__':
    main()
