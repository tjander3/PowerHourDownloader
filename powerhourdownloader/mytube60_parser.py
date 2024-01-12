import logging
import re
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Union

from powerhourdownloader.power_hour import PowerHour
from powerhourdownloader.power_hour_parser import PowerHourParser
from powerhourdownloader.video_link import VideoLink
from powerhourdownloader.youtube_video import YoutubeVideo


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

    def parse(self, debug: Union[bool, str] = False):
        """Parse powerhour given for this class

        Args:
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

        for match_num, match in enumerate(matches, start=1):

            logging.debug(
                "Match {match_num} was found at {start}-{end}: {match}"
                .format(match_num = match_num, start = match.start(), end = match.end(), match = match.group())
            )
            video, start_time, end_time, name = match.groups()
            video = VideoLink(f'https://www.youtube.com/watch?v={video}')
            youtube_video = YoutubeVideo(
                video_link=video,
                name=name,
                video=None,
                start_time=float(start_time),
                end_time=float(end_time),
            )

            videos.append(youtube_video)

        # We do Powerhour instead of a lis of videos here because we may
        # need to parse a video that already has transitions.
        self.power_hour = PowerHour(videos=videos, transitions=None)


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
    mytube60.parse(debug=webpage)

    print(mytube60.power_hour)
    return mytube60


def main():
    example_mytube60_parser_setup()


if __name__ == '__main__':
    main()
