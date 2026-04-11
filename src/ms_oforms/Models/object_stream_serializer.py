from typing import TypeVar
from ms_oforms.Models.control_base import ControlBase


T = TypeVar('T', bound='ObjectStreamSerializer')


class ObjectStreamSerializer:

    def __init__(self: T) -> None:
        self.objects: list[ControlBase] = []

    def to_bytes(self: T) -> bytes:
        output = b''
        for obj in self.objects:
            output += obj.to_bytes()
        return output
