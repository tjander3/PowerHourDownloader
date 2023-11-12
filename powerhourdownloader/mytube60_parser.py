import urllib.request
import requests
from dataclasses import dataclass, field
from pathlib import Path
from xml.etree.ElementTree import fromstring
from lxml import etree

from bs4 import BeautifulSoup

from powerhourdownloader.power_hour import PowerHour
from powerhourdownloader.power_hour_parser import PowerHourParser


@dataclass
class MyTube60Parser(PowerHourParser):
    link: str
    power_hour: PowerHour = field(init=False)

    def _get_webpage(self):
        """Get powerhour webpage from self.link"""
        page = urllib.request.urlopen(self.link)
        webpage_hmtl = page.read()
        return webpage_hmtl

    def parse(self):
        videos = []
        powerhour_webpage = str(self._get_webpage())
        video_list_xpath = '/html/head/script[18]/text()'
        start_of_playlist = powerhour_webpage.find('$(document).ready(function(){\\n\\t\\tplayList = [];')
        end_of_playlist = powerhour_webpage.find("nav = \\\'\\\';\\n\\t\\tfor(var i = 0; i < playList.length; i++){")

        #TODO left off here
        #playList.push({ videoId : 'ap0mqwvf7H0', start : 0.0, end : 61.02097006484987, title : 'Taking Back Sunday - Cute Without the \"E\" (Cut From the Team)' });
        # Need to regex the above string
        # capture videoId, start, end, title
        # then add to videos!

        print(powerhour_webpage[start_of_playlist:end_of_playlist])

        raise NotImplementedError


def main():
    link = 'https://www.mytube60.com/video/on/emo-night/b664367fb7ee40799dccbe693015d6f6.html'

    mytube60 = MyTube60Parser(link=link)
    mytube60.parse()


if __name__ == '__main__':
    main()
