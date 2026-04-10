import struct
from ms_oforms.Models.control_base import ControlBase
from ms_oforms.Enums.data_location import DataLocation
from typing import TypeVar


T = TypeVar('T', bound='MorphData')


class MorphData(ControlBase):
