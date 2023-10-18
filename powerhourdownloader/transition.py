from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from powerhourdownloader.text_video_overlay import TextVideoOverlay


@dataclass
class Transition(ABC):
    video: Path
    text: TextVideoOverlay = None
    audio: str = None  # TODO this needs to be an audio class

    @abstractmethod
    def _add_text_to_video(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _add_audio_to_video(self) -> None:
        raise NotImplementedError
