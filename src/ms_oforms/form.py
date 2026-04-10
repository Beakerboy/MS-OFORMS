from typing import TypeVar
from ms_oforms.Models.control_base import ControlBase


T = TypeVar('T', bound='Form')


class Form:

    def __init__(self: T) -> None:
        self.objects: list[ControlBase] = []

    def write_frx(self: T) -> None:
        # Create o-stream
        # Create f-stream
        # Create ObjCompat
        # Create OLE
        pass
