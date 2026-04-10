from ms_oforms.Models.structure_base import StructureBase
from ms_oforms.Enums.data_location import DataLocation
from typing import TypeVar


T = TypeVar('T', bound='OleSite')


class OleSite(StructureBase):

    SITE_PROP_MAP = {
        0:  ("Name", "<I", DataLocation.BOTH),
        1:  ("TagData", "<I", DataLocation.BOTH),
        2:  ("ID", "<I", DataLocation.DATA_BLOCK),
        3:  ("HelpContextId", "<I", DataLocation.DATA_BLOCK),
        4:  ("BitFlags", "s", DataLocation.DATA_BLOCK),
        5:  ("ObjectStreamSize", "<I", DataLocation.DATA_BLOCK),
        6:  ("TabIndex", "<H", DataLocation.DATA_BLOCK),
        7:  ("ClsidCacheIndex", "<H", DataLocation.DATA_BLOCK),
        8:  ("Position", "<H", DataLocation.EXTRA_BLOCK),
        9:  ("GroupId", "<H", DataLocation.DATA_BLOCK),
        11: ("ControlTipText", "<I", DataLocation.BOTH)
    }
