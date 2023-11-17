from powerhourdownloader.power_hour import PowerHour
from powerhourdownloader.youtube_video import YoutubeVideo
from powerhourdownloader.video_link import VideoLink

import pytest_golden.yaml

pytest_golden.yaml.register_class(PowerHour)
pytest_golden.yaml.register_class(YoutubeVideo)
pytest_golden.yaml.register_class(VideoLink)
