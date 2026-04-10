from enum import Enum, auto


class DataLocation(Enum):
    DATA_BLOCK = auto()
    EXTRA_BLOCK = auto()
    STREAM_DATA = auto()
    NONE = auto()
    BOTH = auto()
