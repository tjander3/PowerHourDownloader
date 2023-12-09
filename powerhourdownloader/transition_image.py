from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from moviepy.editor import ImageClip
from powerhourdownloader.location import Location
from powerhourdownloader.text_video_overlay import TextVideoOverlay
from powerhourdownloader.transition import Transition


@dataclass
class TransitionImage(Transition):
    video: Path
    output: Optional[Path] = None
    updated_video: Path = field(init=False)
    text: Optional[TextVideoOverlay] = None
    audio: Optional[Path] = field(default=None)
    _length: Optional[int] = 3
    image: Path = field(init=False)

    def __post_init__(self):
        self.image = self.video
        # We pass in image to video and then have to convert the name to an mp4 here
        self.video = self.video.parent / f'{self.video.stem}.mp4'

        self._image_to_video()

        # TODO this is shared with trasition_video make one thing to do this
        if self.text is not None:
            self._add_text_to_video()
            # TODO deal with setting this
            self.video = self.updated_video

    def _image_to_video(self) -> None:
        ic = ImageClip(str(self.image)).set_duration(self._length)
        ic.write_videofile(str(self.video), fps=25)  # Many options...

    def _add_audio_to_video(self) -> None:
        raise NotImplementedError


def main():
    ti = TransitionImage(
        video=Path(__file__).parent / '..' / 'tests' / 'images' / 'rory.jpg',
        text=TextVideoOverlay(text='Test')
    )


if __name__ == '__main__':
    main()
