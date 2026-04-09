import struct
from enum import Enum, auto
from typing import TypeVar


T = TypeVar('T', bound='FormControl')


class DataLocation(Enum):
    DATA_BLOCK = auto()
    EXTRA_BLOCK = auto()
    STREAM_DATA = auto()


class FormControl:
    """
    2.2.10.1 FormControl
    """

    FORM_PROP_MAP = {
        0:  ("BackColor", "<I", DataLocation.DATA_BLOCK),
        1:  ("ForeColor", "<I", DataLocation.DATA_BLOCK),
        2:  ("NextID",    "<I", DataLocation.DATA_BLOCK),
        3:  ("Left",      "<i", DataLocation.DATA_BLOCK),
        4:  ("Top",       "<i", DataLocation.DATA_BLOCK),
        5:  ("Width",     "<i", DataLocation.DATA_BLOCK),
        6:  ("Height",    "<i", DataLocation.DATA_BLOCK),
        7:  ("Caption",   "<I", DataLocation.EXTRA_BLOCK),
        8:  ("Font",      "<I", DataLocation.STREAM_DATA),
        9:  ("HelpID",    "<I", DataLocation.DATA_BLOCK),
        10: ("MouseIcon", "<I", DataLocation.STREAM_DATA),
        11: ("Pointer",   "B",   DataLocation.DATA_BLOCK),
        12: ("Tag",       "<I", DataLocation.EXTRA_BLOCK),
        13: ("Picture",   "<I", DataLocation.STREAM_DATA),
        14: ("Zoom",      "<H", DataLocation.DATA_BLOCK),
        15: ("PicAlign",  "B",   DataLocation.DATA_BLOCK),
        16: ("PicTile",   "B",   DataLocation.DATA_BLOCK),
        17: ("PicSize",   "B",   DataLocation.DATA_BLOCK),
        18: ("Cookie",    "<I", DataLocation.DATA_BLOCK),
        19: ("DrawBuf",   "<I", DataLocation.DATA_BLOCK),
        20: ("BordCol",   "<I", DataLocation.DATA_BLOCK),
        21: ("BordStyle", "B",   DataLocation.DATA_BLOCK),
        22: ("Effect",    "B",   DataLocation.DATA_BLOCK),
        23: ("FormSize",  "<I", DataLocation.DATA_BLOCK),
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
    
    :param properties: The dictionary containing current values (e.g., {'Caption': 'Hi'})
    :param prop_map: The mapping of BitIndex -> (Name, ...) used by the parser.
    :return: A 32-bit integer representing the PropMask.
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
