import struct
from typing import TypeVar


T = TypeVar('T', bound='Label')


class Label:

    def __init__(self: T) -> None:
        pass

    def to_bytes(self: T) -> bytes:
        return struct.pack('<BB', 0, 2)
