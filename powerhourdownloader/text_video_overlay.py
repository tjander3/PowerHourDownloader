from dataclasses import dataclass
from typing import Optional
from powerhourdownloader.location import Location
#import Color


@dataclass
class TextVideoOverlay:
    text: str
    text_color: Optional[str] = None  # Color # TODO make this a color Color  # TODO set a default
    text_location: Optional[Location] = None  # TODO set a default
