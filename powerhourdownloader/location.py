from dataclasses import dataclass
from typing import Optional, Union


@dataclass
class Location:
    # Coordinates for where TextOverlay will be placed
    # Default should be the center of the screen
    x: Optional[int] = None
    y: Optional[int] = None
    # To view available str options see documentation for TextClip.set_position
    # from moviepy
    # If x and y are note provided we default to center
    str_loc: Union[tuple[int], tuple[str], str] = 'center'

    def __post_init__(self) -> None:
        # TODO make it so you can only give x,y or str_loc
        if None not in (self.x, self.y):
            self.location = (self.x, self.y)
        else:
            self.location = self.str_loc
