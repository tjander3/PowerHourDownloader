from dataclasses import dataclass
from powerhourdownloader.location import Location
#import Color


@dataclass
class TextVideoOverlay:
    text: str
    text_color: str  # Color # TODO make this a color Color
    text_location: Location
