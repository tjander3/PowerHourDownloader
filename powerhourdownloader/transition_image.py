from dataclasses import dataclass
from pathlib import Path

from powerhourdownloader.text_video_overlay import TextVideoOverlay


@dataclass
class TransitionImage:
    _length: int
    _image: Image  # TODO image
    video: Path
    text: TextVideoOverlay  = None
    audio: Audio  = None  # TODO audio

    def _image_to_video(self) -> None:
        raise NotImplementedError

    def _add_text_to_video(self) -> None:
        raise NotImplementedError

    def _add_audio_to_video(self) -> None:
        raise NotImplementedError
