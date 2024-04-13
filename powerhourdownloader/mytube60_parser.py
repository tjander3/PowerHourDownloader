import logging
import re
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union
from urllib.request import urlopen

from bs4 import BeautifulSoup

from powerhourdownloader.power_hour import PowerHour
from powerhourdownloader.power_hour_parser import PowerHourParser
from powerhourdownloader.video import txt2filename
from powerhourdownloader.video_link import VideoLink, verify_video_link_concurrently
from powerhourdownloader.youtube_audio import YoutubeAudio
from powerhourdownloader.youtube_video import YoutubeVideo
import powerhourdownloader.debug_variables as ph_vars


@dataclass
class MyTube60Parser(PowerHourParser):
    link: Optional[str] = None
    power_hour: PowerHour = field(init=False)

    def _get_webpage(self):
        """Get powerhour webpage from self.link"""
        if not self.link:
            raise ValueError('self.link is expected to be set; not None')

        page = urllib.request.urlopen(self.link)
        webpage_html = page.read()
        return webpage_html

    def get_webpage_title(self):
        if self.test_debug:
            return self.test_debug
        if not self.link:
            raise ValueError('self.link is expected to be set; not None')

        soup = BeautifulSoup(urlopen(self.link))
        title = soup.title.get_text()

        # TODO maybe make a common tool file for txt2filename
        title = txt2filename(title)

        # Go an extra step and remove space in favor of - just since I like that better
        title = title.replace(' ', '-')

        return title

    def parse(self, audio_only: bool = False, debug: Union[bool, str] = False):
        """Parse powerhour given for this class

        Args:
            audio_only (bool): If True we only want audio so we can get rid of video.
                Defaults to False.
            debug (Union[bool, str], optional): Used to test on pre downloaded html file.
                Defaults to False.
                If variable is not false we are expecting webpage content to parse.
        """
        videos = []
        # If debug is not false we are expecting a webpage to have already been provided
        if debug:
            powerhour_webpage = str(debug)
        else:
            powerhour_webpage = str(self._get_webpage())

        start_of_playlist = powerhour_webpage.find('$(document).ready(function(){\\n\\t\\tplayList = [];')
        end_of_playlist = powerhour_webpage.find("nav = \\\'\\\';\\n\\t\\tfor(var i = 0; i < playList.length; i++){")

        regex = r"playList.push\({\svideoId\s:\s\\\'(.+?)\\\',\sstart\s:\s(\d+\.\d+),\send\s:\s(\d+.\d+),\stitle\s:\s\\\'(.+?)\\\'\s}\);"

        test_str = powerhour_webpage[start_of_playlist:end_of_playlist]

        matches = re.finditer(regex, test_str)
        unverified_videos = []

        for match_num, match in enumerate(matches, start=1):
            if ph_vars.debug and (match_num < ph_vars.video_debug[0] or match_num > ph_vars.video_debug[1]):
                continue

            logging.debug(
                "Match {match_num} was found at {start}-{end}: {match}"
                .format(match_num = match_num, start = match.start(), end = match.end(), match = match.group())
            )
            video, start_time, end_time, name = match.groups()
            video = VideoLink(f'https://www.youtube.com/watch?v={video}')

            video_class = YoutubeVideo
            if audio_only:
                video_class = YoutubeAudio

            if ph_vars.main_video_length is not None:
                end_time = str(float(start_time) + ph_vars.main_video_length)

            youtube_video = video_class(
                video_link=video,
                name=name,
                video=None,
                start_time=float(start_time),
                end_time=float(end_time),
            )
            unverified_videos.append(youtube_video)

        # Verify that the video exists and is downloadable
        # TODO is it possible to do this with threads?
        # TODO need to make sure this actually works

        print("verifying videos concurrently")
        results = list(verify_video_link_concurrently(unverified_videos, self))
        print("Done Verifying Videos")
        for link, downloadable in results:
            if not downloadable:
                # Iterate over a copy of the list to safely remove items from the original list
                for obj in unverified_videos[:]:  # my_objects[:] creates a shallow copy of the list
                    if obj.video_link == link:
                        print(f'removing {obj}')
                        unverified_videos.remove(obj)

        videos = unverified_videos

        # We do Powerhour instead of a lis of videos here because we may
        # need to parse a video that already has transitions.
        self.power_hour = PowerHour(videos=videos, transitions=None, title=self.get_webpage_title())


def example_mytube60_parser_setup(
        link='https://www.mytube60.com/video/on/emo-night/b664367fb7ee40799dccbe693015d6f6.html',
        webpage=False,
) -> MyTube60Parser:
    # Link can be used if there is internet connection
    # If no internet connection use the pre downloaded file
    if webpage:
        with open(
            Path(__file__).parent /
            '..' /
            'tests' /
            'webpages' /
            'mytube60-test-webpage-emo-night.html',
            'r',
            encoding='utf-8',
        ) as f:
            link = None
            webpage = f.read()

    mytube60 = MyTube60Parser(link=link)
    mytube60.parse(audio_only=True, debug=webpage)

    print(mytube60.power_hour)
    return mytube60


def main():
    example_mytube60_parser_setup()


if __name__ == '__main__':
    main()
