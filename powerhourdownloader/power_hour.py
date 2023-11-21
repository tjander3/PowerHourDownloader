from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from moviepy.editor import concatenate_videoclips

from powerhourdownloader.video import Video
from powerhourdownloader.transition import Transition


@dataclass
class PowerHour:
    videos: list[Video]
    transitions: Optional[list[Transition]]

    def combine_serially(self):
        for video, transition in zip(self.videos, self.transitions):
            pass

    def combine_in_parallel(self, num_proc: int = 2):
        pass

    def combine_videos(self):
        # concatenating both the clips
        # TODO test this
        # TODO deal with transitions
        videoclips = [item for pair in zip(self.videos, self.transitions) for item in pair]
        final = concatenate_videoclips(videoclips)
        #writing the video into a file / saving the combined video
        final.write_videofile("output.mp4")  # TODO name this better

    def create_power_hour(self) -> Path:
        # TODO left off here lets implemet this, baically loop over all videos and download.  could be good to use multiple cores for this as well
        # download youtube videos
        # stitch videos together
        raise NotImplementedError

    def save_power_hour(self) -> Path:
        raise NotImplementedError

    def upload_power_hour(self) -> None:
        raise NotImplementedError
