from dataclasses import dataclass


@dataclass
class Location:
    # Coordinates for where TextOverlay will be placed
    # Default should be the center of the screen
    x: int = 0
    y: int = 0
