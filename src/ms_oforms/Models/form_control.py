import struct
from enum import Enum, auto
from typing import TypeVar


T = TypeVar('T', bound='FormControl')


class DataLocation(Enum):
    DATA_BLOCK  = auto()
    EXTRA_BLOCK = auto()
    STREAM_DATA = auto()
    NONE        = auto()


class FormControl:
    """
    2.2.10.1 FormControl
    """

    FORM_PROP_MAP = {
        0:  ("Unused1",   "",   DataLocation.NONE),
        1:  ("BackColor", "<I", DataLocation.DATA_BLOCK),
        2:  ("ForeColor", "<I", DataLocation.DATA_BLOCK),
        3:  ("NextID",    "<I", DataLocation.DATA_BLOCK),
        4:  ("Unused2",   "",   DataLocation.NONE),
        5:  ("Unused3",   "",   DataLocation.NONE),
        6:  ("Boolean",     "<i", DataLocation.DATA_BLOCK),
        7:  ("Border",   "<I", DataLocation.DATA_BLOCK),
        8:  ("MousePointer",      "<I", DataLocation.DATA_BLOCK),
        9:  ("ScrollBars",    "<I", DataLocation.DATA_BLOCK),
        10: ("Display", "<I", DataLocation.EXTRA_BLOCK),
        11: ("LogicalSize",   "B",   DataLocation.EXTRA_BLOCK),
        12: ("ScrollPosition",       "<I", DataLocation.EXTRA_BLOCK),
        13: ("Group",   "<I", DataLocation.STREAM_DATA),
        14: ("Reserved",      "<H", DataLocation.DATA_BLOCK),
        15: ("MouseIcon",  "B",   DataLocation.DATA_BLOCK),
        16: ("Cycle",   "B",   DataLocation.DATA_BLOCK),
        17: ("SpecialEffect",   "B",   DataLocation.DATA_BLOCK),
        18: ("BorderColor",    "<I", DataLocation.DATA_BLOCK),
        19: ("Caption",   "<I", DataLocation.DATA_BLOCK),
        20: ("Font",   "<I", DataLocation.DATA_BLOCK),
        21: ("Picture", "B",   DataLocation.DATA_BLOCK),
        22: ("Zoom",    "B",   DataLocation.DATA_BLOCK),
        23: ("PictureAligmment",  "", DataLocation.DATA_BLOCK),
        24: ("PictureTiling", "", DataLocation.DATA_BLOCK),
        25: ("PictureSizeMode", "", DataLocation.DATA_BLOCK),
        26: ("ShapeCookie", "", DataLocation.DATA_BLOCK),
        27: ("DrawBuffer", "", DataLocation.DATA_BLOCK)
    }

    def __init__(self: T) -> None:
        self._min_ver = 0
        self._maj_ver = 4
        self.properties = {}

    def to_bytes(self: T) -> bytes:
        output = (
            struct.pack(
                '<BBI', self._min_ver, self._maj_ver, self.generate_prop_mask
            ) + self.data + self.extra +
            self.stream_data + self.site_data +
            self.design_ex_data
        )
        return output

    def generate_prop_mask(self: T) -> int:
        """
        Recreates a 4-byte PropMask bitfield based on a dictionary of properties.
        """
        mask = 0
    
        # Iterate through the known mapping for this object type
        for bit, map_data in self.FORM_PROP_MAP.items():
            # Get the property name from the map (usually the first element)
            prop_name = map_data[0] if isinstance(map_data, tuple) else map_data
        
            # If the property exists in the dict and is not None, set the bit
            if prop_name in self.properties and self.properties[prop_name] is not None:
                mask |= (1 << bit)
            
        return mask
