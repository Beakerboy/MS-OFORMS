from typing import TypeVar
from ms_oforms.Models.control_base import ControlBase


T = TypeVar('T', bound='Form')


class Form:

    def __init__(self: T) -> None:
        self._objects: list[ControlBase] = []

    def add_control(self: T, control: ControlBase) -> None:
        control.properties["ID"] = len(self._objects) + 1
        control.properties["TabIndex"] = len(self._objects)
        self._objects.append([control])
        
    def write_frx(self: T) -> None:
        # Create o-stream
        # Create f-stream
        # Create ObjCompat
        # Create OLE
        # Prepend 24 bytes
        pass
