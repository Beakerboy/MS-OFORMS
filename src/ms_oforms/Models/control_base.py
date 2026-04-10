from ms_oforms.Models.structure_base import StructureBase
from ms_oforms.Models.text_props import TextProps
from typing import TypeVar


T = TypeVar('T', bound='ControlBase')


class ControlBase(StructureBase):
    """
    A Control is a Structure with TextProps
    """

    ClsidCacheIndex = 0x7fff

    def to_bytes(self: T) -> bytes:
        text_props = TextProps()
        text_props.properties = self.properties
        return super().to_bytes() + text_props.to_bytes()
