from pathlib import Path


class YoutubeVideo:
    def __init__(self) -> None:
        raise NotImplementedError

    def download(self, start_time=None, end_time=None) -> Path
        raise NotImplementedError
