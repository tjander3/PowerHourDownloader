from abc import ABC, abstractmethod


class Transition(ABC):
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _add_text_to_video(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def _add_audio_to_video(self) -> None:
        raise NotImplementedError
