from dataclasses import dataclass
from typing import Optional
from powerhourdownloader.location import Location
#import Color


@dataclass
class TextVideoOverlay:
    text: str
    text_color: Optional[str] = 'black'  # Color # TODO make this a color Color  # TODO set a default
    text_location: Optional[Location] = None

    def __post_init__(self):
        # TODO better way to do default for dataclass?
        if self.text_location is None:
            self.text_location = Location()
