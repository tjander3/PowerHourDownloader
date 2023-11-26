import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from moviepy.editor import concatenate_videoclips, VideoFileClip

from powerhourdownloader.transition import Transition
from powerhourdownloader.video import Video


@dataclass
class PowerHour:
    videos: list[Video]
    transitions: Optional[list[Optional[Transition]]]

    def combine_serially(self):
        for video, transition in zip(self.videos, self.transitions):
            pass

    def combine_in_parallel(self, num_proc: int = 2):
        pass

    def combine_videos(self):
        # concatenating both the clips
        # TODO test this
        # TODO combination created a problem
        if self.transitions is None:
            self.transitions = [None for _ in range(len(self.videos))]

        videoclips = [
            VideoFileClip(str(item.video))
            for pair in zip(self.videos, self.transitions)
            for item in pair if item is not None
        ]
        # TODO can this be used to do in parallel
        final = concatenate_videoclips(videoclips)
        #writing the video into a file / saving the combined video
        final.write_videofile("output.mp4")  # TODO name this better

    def create_power_hour(self) -> Path:
        # TODO left off here lets implemet this, baically loop over all videos and download.  could be good to use multiple cores for this as well
        # download youtube videos
        # stitch videos together
        # TODO option to download in parallel?
        for video in self.videos:
            logging.debug('Downloading %s', video.name)
            video.download()

        self.combine_videos()

    def save_power_hour(self) -> Path:
        raise NotImplementedError

    def upload_power_hour(self) -> None:
        raise NotImplementedError

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    from powerhourdownloader.mytube60_parser import \
        example_mytube60_parser_setup
    power_hour_parser = example_mytube60_parser_setup()
    # Create a tmp power hour from example in other class. We just
    # want to make a short power hour with a few videos so this main
    # function can run faster
    power_hour_tmp = power_hour_parser.power_hour

    power_hour = PowerHour(videos=power_hour_tmp.videos[0:3], transitions=None)
    power_hour.create_power_hour()


if __name__ == '__main__':
    main()
