from powerhourdownloader.location import Location


@dataclass
class TextVideoOverlay:
    text: str
    text_color: str # TODO make this a color Color
    text_location: Location
