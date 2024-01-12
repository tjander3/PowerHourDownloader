import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from powerhourdownloader.video_link import VideoLink


# TODO not sure the best place to put this yet
# From here https://stackoverflow.com/a/65360714
def txt2filename(txt, chr_set='printable'):
    """Converts txt to a valid filename.

    Args:
        txt: The str to convert.
        chr_set:
            'printable':    Any printable character except those disallowed on Windows/*nix.
            'extended':     'printable' + extended ASCII character codes 128-255
            'universal':    For almost *any* file system. '-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    """

    FILLER = '-'
    START_FILLER = 'x'
    MAX_LEN = 255  # Maximum length of filename is 255 bytes in Windows and some *nix flavors.

    # Step 1: Remove excluded characters.
    BLACK_LIST = set(chr(127) + r'<>:"/\|?*')                           # 127 is unprintable, the rest are illegal in Windows.
    white_lists = {
        'universal': {'-.0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'},
        'printable': {chr(x) for x in range(32, 127)} - BLACK_LIST,     # 0-32, 127 are unprintable,
        'extended' : {chr(x) for x in range(32, 256)} - BLACK_LIST,
    }
    white_list = white_lists[chr_set]
    result = ''.join(x
                     if x in white_list else FILLER
                     for x in txt)

    # Step 2: Device names, '.', and '..' are invalid filenames in Windows.
    DEVICE_NAMES = 'CON,PRN,AUX,NUL,COM1,COM2,COM3,COM4,' \
                   'COM5,COM6,COM7,COM8,COM9,LPT1,LPT2,' \
                   'LPT3,LPT4,LPT5,LPT6,LPT7,LPT8,LPT9,' \
                   'CONIN$,CONOUT$,..,.'.split(',')  # This list is an O(n) operation.
    if result in DEVICE_NAMES:
        result = f'{FILLER}{result}{FILLER}'

    # Step 3: Truncate long files while preserving the file extension.
    if len(result) > MAX_LEN:
        if '.' in txt:
            result, _, ext = result.rpartition('.')
            ext = '.' + ext
        else:
            ext = ''
        result = result[:MAX_LEN - len(ext)] + ext

    # Step 4: Windows does not allow filenames to end with '.' or ' ' or begin with ' '.
    # I also dont want to allow - or * for ffmpeg running into problems writing possibly
    result = re.sub(r'^[. -*]', START_FILLER, result)
    result = re.sub(r' $', FILLER, result)

    return result


@dataclass
class Video(ABC):
    video_link: VideoLink
    name: Optional[str]
    video: Optional[Path]
    start_time: Optional[float]
    end_time: Optional[float]

    def setup_download_dir(self) -> None:
        # If self.video is not provided this will set it and make sure
        # it exists
        self.video = Path(__file__).parent / 'videos'
        self.video.mkdir(parents=True, exist_ok=True)
        self.video = self.video / f'{txt2filename(self.name)}.mp4'

    @abstractmethod
    def download(self) -> Path:
        raise NotImplementedError
