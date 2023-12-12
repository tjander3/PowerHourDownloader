import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from moviepy.editor import concatenate_videoclips, VideoFileClip
from powerhourdownloader.location import Location
from powerhourdownloader.text_video_overlay import TextVideoOverlay

from powerhourdownloader.transition import Transition
from powerhourdownloader.transition_video import TransitionVideo
from powerhourdownloader.video import Video
from powerhourdownloader.video_link import VideoLink
from powerhourdownloader.youtube_video import YoutubeVideo


@dataclass
class PowerHour:
    videos: list[Video]
    # Transitions can either be None, a single transition to be used between
    # all videos or a list of transitions.  The list of transitions can also
    # have None if you dont want a transition in between certain videos
    transitions: Optional[Union[Transition, list[Optional[Transition]]]]
    output: Path = Path(__file__).parent / 'videos' / 'tyler-output.mp4'

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
        self._set_transitions()

        videoclips = [
            VideoFileClip(str(item.video))
            for pair in zip(self.videos, self.transitions)
            for item in pair if item is not None
        ]
        # TODO can this be used to do in parallel
        # Fix concatenate thanks to following links
        # https://stackoverflow.com/questions/45248042/moviepy-concatenating-video-clips-causes-weird-glitches-in-final-video
        # https://www.reddit.com/r/moviepy/comments/2z3q38/help_getting_glitch_art_when_concatenating_clips/
        final = concatenate_videoclips(videoclips, method='compose')
        # writing the video into a file / saving the combined video
        final.write_videofile(str(self.output))  # TODO name this better

    def create_power_hour(self) -> None:
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
