from typing import TypeVar
from ms_oforms.Models.control_base import ControlBase


T = TypeVar('T', bound='Form')


class Form:

    default_props = {
        "BooleanProperties": 4
    }

    def __init__(self: T) -> None:
        self._properties = self.default_props.copy()
        self._objects: list[ControlBase] = []

    def add_control(self: T, control: ControlBase) -> None:
        control.properties["ID"] = len(self._objects) + 1
        control.properties["TabIndex"] = len(self._objects)
        control.properties["ObjectStreamSize"] = len(control.to_bytes())
        control.properties["ClsidCacheIndex"] = control.ClsidCacheIndex
        self._objects.append(control)

    def enable_form(self: T) -> None:
        self._properties["BooleanProperties"] |= 4

    def disable_form(self: T) -> None:
        self._properties["BooleanProperties"] ^= 4

    def write_frx(self: T) -> None:
        # Create o-stream
        # Create f-stream
        # Create ObjCompat
        # Create OLE
        # Prepend 24 bytes
        pass
