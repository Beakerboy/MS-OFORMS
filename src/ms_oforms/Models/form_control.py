import struct
from enum import Enum, auto
from typing import TypeVar


T = TypeVar('T', bound='FormControl')


class DataLocation(Enum):
    DATA_BLOCK = auto()
    EXTRA_BLOCK = auto()
    STREAM_DATA = auto()
    NONE = auto()
    BOTH = auto()


class FormControl:
    """
    2.2.10.1 FormControl
    """

    # All DATA_BLOCK data is for bytes.
    FORM_PROP_MAP = {
        0:  ("Unused1",        "",   DataLocation.NONE),
        1:  ("BackColor",      "", DataLocation.DATA_BLOCK),
        2:  ("ForeColor",      "", DataLocation.DATA_BLOCK),
        3:  ("NextID",         "", DataLocation.DATA_BLOCK),
        4:  ("Unused2",        "",  DataLocation.NONE),
        5:  ("Unused3",        "",   DataLocation.NONE),
        6:  ("Boolean",        "", DataLocation.DATA_BLOCK),
        7:  ("Border",         "", DataLocation.DATA_BLOCK),
        8:  ("MousePointer",   "", DataLocation.DATA_BLOCK),
        9:  ("ScrollBars",     "", DataLocation.DATA_BLOCK),
        10: ("Display",        "<Q", DataLocation.EXTRA_BLOCK),
        11: ("LogicalSize",    "<Q",   DataLocation.EXTRA_BLOCK),
        12: ("ScrollPosition", "<Q", DataLocation.EXTRA_BLOCK),
        13: ("Group",   "<I", DataLocation.STREAM_DATA),
        14: ("Reserved",      "<H", DataLocation.DATA_BLOCK),
        15: ("MouseIcon",  "B",   DataLocation.DATA_BLOCK),
        16: ("Cycle",   "B",   DataLocation.DATA_BLOCK),
        17: ("SpecialEffect",   "B",   DataLocation.DATA_BLOCK),
        18: ("BorderColor",    "<I", DataLocation.DATA_BLOCK),
        19: ("Caption",   "", DataLocation.BOTH),
        20: ("Font",   "<I", DataLocation.STREAM_DATA),
        21: ("Picture", "B",   DataLocation.STREAM_DATA),
        22: ("Zoom",    "B",   DataLocation.DATA_BLOCK),
        23: ("PictureAligmment",  "", DataLocation.DATA_BLOCK),
        24: ("PictureTiling", "", DataLocation.DATA_BLOCK),
        25: ("PictureSizeMode", "", DataLocation.DATA_BLOCK),
        26: ("ShapeCookie", "", DataLocation.DATA_BLOCK),
        27: ("DrawBuffer", "", DataLocation.DATA_BLOCK)
    }

    SITE_PROP_MAP = {
        0:  ("Name", "<I", DataLocation.DATA_BLOCK),
        1:  ("TagData", "<I", DataLocation.DATA_BLOCK),
        2:  ("ID", "<I", DataLocation.DATA_BLOCK),
        3:  ("HelpContextId", "<I", DataLocation.DATA_BLOCK),
        4:  ("BitFlags", "<I", DataLocation.DATA_BLOCK),
        5:  ("ObjectStreamSize", "<I", DataLocation.DATA_BLOCK),
        6:  ("TabIndex", "<H", DataLocation.DATA_BLOCK),
        7:  ("ClsidCacheIndex", "<H", DataLocation.DATA_BLOCK),
        8:  ("GroupId", "<H", DataLocation.DATA_BLOCK)
    }

    def __init__(self: T) -> None:
        self._min_ver = 0
        self._maj_ver = 4
        self.properties = {}
        self.class_table = []
        self.sites = []

    def to_bytes(self: T) -> bytes:
        data = self.generate_data_block()
        extra = self.generate_extra_data_block()
        stream = self.generate_stream_data()
        site = self.generate_site_data()
        cb_form = 4 + len(data) + len(extra)
        output = (
            struct.pack(
                '<BBHI', self._min_ver, self._maj_ver, cb_form,
                self.generate_prop_mask()
            ) + data + extra + stream + site
        )
        return output

    def generate_data_block(self: T) -> bytes:
        output = b''
        for bit, map_data in self.FORM_PROP_MAP.items():
            if (
                    (map_data[2] == DataLocation.DATA_BLOCK or
                     map_data[2] == DataLocation.BOTH) and
                    map_data[0] in self.properties
            ):
                if map_data[2] == DataLocation.BOTH:
                    val = self.properties[map_data[0]][0]
                else:
                    val = self.properties[map_data[0]]
                output += struct.pack('<I', val)
        return output

    def generate_extra_data_block(self: T) -> bytes:
        output = b''
        for bit, map_data in self.FORM_PROP_MAP.items():
            if (
                    (map_data[2] == DataLocation.EXTRA_BLOCK or
                     map_data[2] == DataLocation.BOTH) and
                    map_data[0] in self.properties
            ):
                if map_data[2] == DataLocation.BOTH:
                    val = self.properties[map_data[0]][1]
                else:
                    val = self.properties[map_data[0]]
                output += struct.pack('<Q', val)
        return output

    def generate_stream_data(self: T) -> bytes:
        output = b''
        for bit, map_data in self.FORM_PROP_MAP.items():
            if (
                    map_data[2] == DataLocation.STREAM_DATA and
                    map_data[0] in self.properties
            ):
                val = self.properties[map_data[0]]
                output += struct.pack('<Q', val)
        return output

    def generate_site_data(self: T) -> bytes:
        output = struct.pack('<H', len(self.class_table))
        site_records = b''
        for site in self.sites:
            site_data = b''
            for map_data in self.SITE_PROP_MAP:
                name = map_data[0]
                if name in site[1]:
                    site_data += site[1][name]
            site_extra = site[2]
            site_records += (
                struct.pack('<HHH', 0, 4 + len(site_data) + len(site_extra), site[0]) +
                site_data + site_extra
            )
        depth = self.depth
        pad_size = min(4 - len(depth) % 4, 3)
        padded_depth = depth + b't' * pad_size
        count_of_bytes = len(padded_depth) + len(site_records)
        for item in self.class_table:
            output += item
        output += struct.pack('<II', len(self.sites), count_of_bytes)
        output += padded_depth + site_records
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
