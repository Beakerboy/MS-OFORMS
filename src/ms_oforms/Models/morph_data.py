import struct
from ms_oforms.Models.control_base import ControlBase
from ms_oforms.Enums.data_location import DataLocation
from typing import TypeVar


T = TypeVar('T', bound='MorphData')


class MorphData(ControlBase):

    PROP_MAP = {
        0:  ("Various", "<I", DataLocation.DATA_BLOCK),
        1:  ("BackColor", "<I", DataLocation.DATA_BLOCK),
        2:  ("ForeColor", "<I", DataLocation.DATA_BLOCK),
        3:  ("MaxLength", "<I", DataLocation.DATA_BLOCK),
        4:  ("BorderStyle", "<B", DataLocation.DATA_BLOCK),
        5:  ("Scrollbars", "<B", DataLocation.DATA_BLOCK),
        6:  ("DisplayStyle", "<B", DataLocation.DATA_BLOCK),
        7:  ("MousePointer", "<B", DataLocation.DATA_BLOCK),
        8:  ("Size", "<H", DataLocation.EXTRA_BLOCK),
        9:  ("PasswordChar", "<H", DataLocation.DATA_BLOCK),
        11: ("ListWidth", "<I", DataLocation.DATA_BLOCK)
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
                        extra += self.compress_and_pad(value)
                    elif map_data[2] == DataLocation.DATA_BLOCK:
                        if map_data[1] == "s":
                            data += value
                        else:
                            data += struct.pack(map_data[1], value)
                    elif map_data[2] == DataLocation.EXTRA_BLOCK:
                        extra += self.compress_and_pad(value)
        cb_label = 8 + len(data) + len(extra)
        prop_mask = self.generate_prop_mask()
        return (
            struct.pack('<BBHQ', 0, 2, cb_label, prop_mask) +
            data + extra
        )
