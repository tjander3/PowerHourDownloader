from abc import ABC, abstractmethod
from pathlib import Path


class Video(ABC):
    def __init__(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def download(self, start_time=None, end_time=None) -> Path
        raise NotImplementedError
