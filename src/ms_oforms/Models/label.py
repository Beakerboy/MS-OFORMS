import struct
from typing import TypeVar


T = TypeVar('T', bound='Label')


class Label:

    def __init__(self: T) -> None:
        self.data = b''
        self.extended = b''

    def to_bytes(self: T) -> bytes:
        cb_label = 4 + len(self.data) + len(self.extended)
        return struct.pack('<BBH', 0, 2, cb_label)
