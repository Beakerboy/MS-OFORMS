from typing import TypeVar


T = TypeVar('T', bound='FormEmbedded')


class FormEmbedded:

    def to_bytes(self: T) -> bytes:
        return b''
