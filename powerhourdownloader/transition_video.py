from dataclasses import dataclass
from pathlib import Path
from powerhourdownloader.text_video_overlay import TextVideoOverlay
from powerhourdownloader.transition import Transition


@dataclass
class TransitionVideo(Transition):
    video: Path
    text: TextVideoOverlay = None
    audio: Audio = None  # TODO audio

    def _add_text_to_video(self) -> None:
        raise NotImplementedError

    def _add_audio_to_video(self) -> None:
        raise NotImplementedError
