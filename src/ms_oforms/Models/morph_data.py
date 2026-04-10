import struct
from ms_oforms.Models.control_base import ControlBase
from ms_oforms.Enums.data_location import DataLocation
from typing import TypeVar


T = TypeVar('T', bound='MorphData')


class MorphData(ControlBase):

    PROP_MAP = {
        0:  ("Various", "s", DataLocation.DATA_BLOCK),
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
        super().__init__()
        self.prop_mask_size = 8
        self.properties = {}

    def to_bytes(self: T) -> bytes:
        text_props = TextProps()
        text_props.properties = self.properties
        return (
            super().to_bytes() +
            text_props.to_bytes()
        )

    def generate_prop_mask(self: T) -> int:
        return super().generate_prop_mask() | (1 << 31)
