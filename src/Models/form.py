import struct
from typing import TypeVar


T = TypeVar('T', bound='Form')


class Form:

    def __init__(self: T) -> None:
        self._min_ver = 0
        self._maj_ver = 4

    def to_bytes(self: T) -> bytes:
        output = (
            struct.pack(
                '<BB', self._min_ver, self._maj_ver
            ) + self.data + self.extra +
            self.stream_data + self.site_data +
            self.design_ex_data
        )
        return output
        
