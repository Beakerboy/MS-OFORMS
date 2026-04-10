import struct
from ms_oforms.Models.structure_base import StructureBase
from ms_oforms.Enums.data_location import DataLocation
from typing import TypeVar


T = TypeVar('T', bound='TextProps')


class TextProps(StructureBase):

    PROP_MAP = {
        0:  ("FontName", "<I", DataLocation.BOTH),
        1:  ("FontEffects", "<I", DataLocation.DATA_BLOCK),
        2:  ("FontHeight", "<I", DataLocation.DATA_BLOCK),
        4:  ("FontCharset", "<B", DataLocation.DATA_BLOCK),
        5:  ("FontPitchAndFamily", "<B", DataLocation.DATA_BLOCK),
    }
