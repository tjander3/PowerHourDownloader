import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from moviepy.editor import CompositeVideoClip, TextClip, VideoFileClip

# TODO figure out why this is not importing
from powerhourdownloader.text_video_overlay import TextVideoOverlay
from powerhourdownloader.transition import Transition


@dataclass
class TransitionVideo():#Transition):
    video: Path
    text: Optional[TextVideoOverlay] = None
    audio: Optional[Path] = field(default=None)

    def _add_text_to_video(self) -> None:
        # TODO this could be in the parent class
        # Python program to write
        # text on video
        if self.text is None:
            # If there is no text to add do not do anything
            return

        video_path = Path(__file__).parent / '..' / 'videos' / 'hello-there.mp4'
        logging.debug(video_path.absolute())
        if video_path.exists():
            logging.debug(f'video exist: {video_path.exists()}')
        else:
            logging.error(f'video does not exist: {video_path.exists()}')

        video = VideoFileClip(str(video_path))

        # Make the text. Many more options are available.
        txt_clip = (
            # TODO use text video overlay instead
            TextClip(self.text.text, fontsize=70, color='white')
                .set_position('center')  # TODO set this myself with text_video_overlay
                .set_duration(10)  # TODO we need to have a duration
        )

        result = CompositeVideoClip([video, txt_clip])  # Overlay text on video
        # TODO find out original video fps?
        # TODO what name to use
        result.write_videofile(str(video_path.parent / f'text-added-{video_path.name}'), fps=25)  # Many options...


    def _add_audio_to_video(self) -> None:
        raise NotImplementedError

def main():
    tv = TransitionVideo(
        video='',
        text=TextVideoOverlay(text='Hello there'),
        audio='xxx'
    )
    tv._add_text_to_video()

if __name__ == '__main__':
    main()
