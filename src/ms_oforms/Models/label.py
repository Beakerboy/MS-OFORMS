import struct
from ms_oforms.Models.control_base import ControlBase
from ms_oforms.Models.text_props import TextProps
from ms_oforms.Enums.data_location import DataLocation
from typing import TypeVar


T = TypeVar('T', bound='Label')


class Label(ControlBase):

    PROP_MAP = {
        0:  ("ForeColor", "<I", DataLocation.DATA_BLOCK),
        1:  ("BackColor", "<I", DataLocation.DATA_BLOCK),
        2:  ("Various", "<I", DataLocation.DATA_BLOCK),
        3:  ("Caption", "<I", DataLocation.BOTH),
        4:  ("PicturePosition", "s", DataLocation.DATA_BLOCK),
        5:  ("Size", "<I", DataLocation.EXTRA_BLOCK),
        6:  ("MousePointer", "<H", DataLocation.DATA_BLOCK),
        7:  ("BorderColor", "<H", DataLocation.DATA_BLOCK),
        8:  ("BorderStyle", "<H", DataLocation.EXTRA_BLOCK),
        9:  ("SpecialEffect", "<H", DataLocation.DATA_BLOCK),
        11: ("Picture", "<I", DataLocation.BOTH)
    }
    
    def __init__(self: T) -> None:
        self.properties = {}
        self.text_props = TextProps()

    def to_bytes(self: T) -> bytes:
        return (
            super().to_bytes() +
            self.text_props.to_bytes()
        )
