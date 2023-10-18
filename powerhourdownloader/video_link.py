from dataclasses import dataclass


@dataclass
class VideoLink:
    video_link: str

    def verify_video_link(self) -> bool:
        raise NotImplementedError
