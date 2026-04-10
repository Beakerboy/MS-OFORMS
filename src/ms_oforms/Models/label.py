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
        self.extended = b''
        self.properties = {}

    def to_bytes(self: T) -> bytes:
        data = b''
        for bit, map_data in self.PROP_MAP.items():
                name = map_data[0]
                if name in self.properties:
                    if map_data[2] == DataLocation.BOTH:
                        value = len(site[1][name]) | 0x80000000
                        data += struct.pack("<I", value)
                        extra += site[1][name]
                    elif map_data[2] == DataLocation.DATA_BLOCK:
                        if map_data[1] == "s":
                            site_data += site[1][name]
                        else:
                            site_data += struct.pack(map_data[1], site[1][name])
                    elif map_data[2] == DataLocation.EXTRA_BLOCK:
                        site_extra += site[1][name]
        cb_label = 4 + len(self.data) + len(self.extended)
        prop_mask = self.generate_prop_mask()
        return struct.pack('<BBHI', 0, 2, cb_label, prop_mask)
