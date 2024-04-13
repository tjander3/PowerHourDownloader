try:
    from enum import StrEnum
except ImportError:
    from strenum import StrEnum  # type: ignore

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from moviepy.editor import concatenate_videoclips, VideoFileClip, AudioFileClip, concatenate_audioclips
from powerhourdownloader.location import Location
from powerhourdownloader.text_video_overlay import TextVideoOverlay

from powerhourdownloader.transition import Transition
from powerhourdownloader.transition_video import TransitionVideo
from powerhourdownloader.video import Video
from powerhourdownloader.video_link import VideoLink
from powerhourdownloader.youtube_audio import YoutubeAudio
from powerhourdownloader.youtube_video import YoutubeVideo
import powerhourdownloader.debug_variables as ph_vars

class DownloadStatusEnum(StrEnum):
    WAITING = 'Waiting to start downloading'
    VERIFYING_VIDEOS = 'Verifying Videos Exist'
    VIDEOS_DOWNLOADING = 'Videos Downloading'
    VIDEOS_COMBINING = 'Combining videos'
    VIDEOS_WRITING = 'Writing the Videos to file'
    VIDEOS_DONE = 'Done with the power hour'


@dataclass
class PowerHour:
    videos: list[Video]
    # Transitions can either be None, a single transition to be used between
    # all videos or a list of transitions.  The list of transitions can also
    # have None if you dont want a transition in between certain videos
    transitions: Optional[Union[Transition, list[Optional[Transition]]]]
    output: Path = Path(__file__).parent / 'videos' / 'tyler-output.mp4'
    title: Optional[str] = None
    videos_downloaded: int = 0  # TODO should not be able to set this as a parameter
    power_hour_status: DownloadStatusEnum = DownloadStatusEnum.WAITING  # TODO should not be able to set this as a parameter
    total_videos: Optional[int] = None  # TODO should not be able to set this as a parameter

    def __post_init__(self):
        if self.title:
            # Rename the file to use the webpages name, make sure to keep the file extension
            # of current output
            file_extension = self.output.suffix
            self.output = self.output.resolve().parent / f'{self.title}{file_extension}'

    def combine_serially(self):
        for video, transition in zip(self.videos, self.transitions):
            pass

    def combine_videos_in_parallel(self, num_proc: int = 2):
        raise NotImplementedError

    def _set_transitions(self):
        if self.transitions is None:
            self.transitions = [None for _ in range(len(self.videos))]
        elif isinstance(self.transitions, Transition):
            self.transitions = [self.transitions for _ in range(len(self.videos))]
        elif isinstance(self.transitions, list):
            # self.transitions is already set no need to do anything
            pass
        else:
            raise ValueError(f'self.transitions is an unexpected value: {self.transitions}')


    def combine_videos(self) -> None:
        # concatenating both the clips and store results in self.output
        # TODO test this
        # TODO need to cleanup videos as well
        # TODO ability to set one transition
        self.power_hour_status = DownloadStatusEnum.VIDEOS_COMBINING

        self._set_transitions()

        clip_type = VideoFileClip
        if isinstance(self.videos[0], YoutubeAudio):
            clip_type = AudioFileClip
        videoclips = [
            clip_type(str(item.video))
            for pair in zip(self.videos, self.transitions)
            # Here we are skipping and transitions or videos that are not complete.
            # It would be great if we kept track of them and printed a report or message
            # letting the user know something went wrong
            for item in pair if item is not None and item.video is not None
        ]
        # TODO can this be used to do in parallel
        # Fix concatenate thanks to following links
        # https://stackoverflow.com/questions/45248042/moviepy-concatenating-video-clips-causes-weird-glitches-in-final-video
        # https://www.reddit.com/r/moviepy/comments/2z3q38/help_getting_glitch_art_when_concatenating_clips/

        # TODO combine better somehow, aka use classes or something
        if isinstance(self.videos[0], YoutubeAudio):
            final = concatenate_audioclips(videoclips)
            self.output = self.output.with_suffix('.mp3')
            self.power_hour_status = DownloadStatusEnum.VIDEOS_WRITING
            final.write_audiofile(str(self.output))  # TODO name this better
        else:
            final = concatenate_videoclips(videoclips, method='compose')
            self.power_hour_status = DownloadStatusEnum.VIDEOS_WRITING
            final.write_videofile(str(self.output))  # TODO name this better

        # writing the video into a file / saving the combined video

    def create_power_hour(self) -> None:
        # download youtube videos
        # stitch videos together
        # TODO option to download in parallel?

        # Here we set self.videos to only be 3 vidoes so downloading and combining can
        # happen faster.  When committing please make sure this is False
        # TODO would be great if this was set at class level or by some command line argument
        # or some bash variable
        if ph_vars.debug:
            pass
            # THis will already be taken care of in other location
            # self.videos = self.videos[ph_vars.video_debug[0]:ph_vars.video_debug[1]]

        # TODO make this downloaing its own function
        self.power_hour_status = DownloadStatusEnum.VIDEOS_DOWNLOADING
        self.total_videos = len(self.videos)
        for index, video in enumerate(self.videos):
            logging.debug('Video #%s', index)
            logging.debug('Downloading %s', video.name)
            # TODO try catch on video .download, if fail change videos downloaded and totatl _videos appropriately
            video.download()
            #logging.error('Download Failed')
            self.videos_downloaded += 1

        self.combine_videos()

        self.power_hour_status = DownloadStatusEnum.VIDEOS_DONE

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

    # TODO create a function in transition video and transition image to be used for this
    transition_video = YoutubeVideo(
        video_link=VideoLink(video_link='https://www.youtube.com/watch?v=XfzAB1lDGgg'),
        name=None,
        video=None,
        start_time=None,
        end_time=None,
    )
    transition_video.download()
    transition = TransitionVideo(
        video=transition_video.video,
        text=TextVideoOverlay(
            text='Drink!',
            text_color='black',
            text_location=Location(str_loc=('left', 'top')),
        ),
    )

    power_hour = PowerHour(videos=power_hour_tmp.videos[0:2], transitions=transition)
    power_hour.create_power_hour()


if __name__ == '__main__':
    main()
