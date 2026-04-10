from typing import TypeVar


T = TypeVar('T', bound='FormEmbedded')


class FormEmbedded:

    def to_bytes(self: T) -> bytes:
        output = b''
        for obj in self.objects:
            output += obj.to_bytes()
        return output
