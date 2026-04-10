from typing import TypeVar


T = TypeVar('T', bound='Form')


class Form:

    def __init__(self: T) -> None:
        self.objects = []

    def write_frx(self: T) -> None:
        # Create o-stream
        # Create f-stream
        # Create ObjCompat
        # Create OLE
        pass
