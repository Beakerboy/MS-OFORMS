from ms_oforms.Models.control_base import ControlBase
from ms_oforms.Enums.data_location import DataLocation
from typing import TypeVar


T = TypeVar('T', bound='CommandButton')


class CommandButton(ControlBase):

    PROP_MAP = {
        0:  ("ForeColor", "<I", DataLocation.DATA_BLOCK),
        1:  ("BackColor", "<I", DataLocation.DATA_BLOCK),
        2:  ("Various", "<I", DataLocation.DATA_BLOCK),
        3:  ("Caption", "<I", DataLocation.BOTH),
        4:  ("PicturePosition", "<I", DataLocation.DATA_BLOCK),
        5:  ("Size", "<I", DataLocation.EXTRA_BLOCK),
        6:  ("MousePointer", "<H", DataLocation.DATA_BLOCK),
        7:  ("Picture", "<H", DataLocation.DATA_BLOCK),
        8:  ("Accelerator", "<H", DataLocation.EXTRA_BLOCK),
        9:  ("TakeFocusOnClick", "<H", DataLocation.DATA_BLOCK),
        10: ("MouseIcon", "<I", DataLocation.BOTH)
    }

    ClsidCacheIndex = 0x11
