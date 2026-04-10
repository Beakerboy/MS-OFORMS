import struct
from ms_oforms.Models.control_base import ControlBase
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

    def to_bytes(self: T) -> bytes:
        data = b''
        extra = b''
        for bit, map_data in self.PROP_MAP.items():
                name = map_data[0]
                if name in self.properties:
                    value = self.properties[name]
                    if map_data[2] == DataLocation.BOTH:
                        cba = len(value) | 0x80000000
                        data += struct.pack("<I", cba)
                        extra += Label.compress_and_pad(value)
                    elif map_data[2] == DataLocation.DATA_BLOCK:
                        if map_data[1] == "s":
                            data += value
                        else:
                            data += struct.pack(map_data[1], value)
                    elif map_data[2] == DataLocation.EXTRA_BLOCK:
                        extra += Label.compress_and_pad(value)
        cb_label = 4 + len(data) + len(extra)
        prop_mask = self.generate_prop_mask()
        return (
            struct.pack('<BBHI', 0, 2, cb_label, prop_mask) +
            data + extra
        )
