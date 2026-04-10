import struct
import io
from enum import Enum, auto
from typing import Dict, List, Any

class DataLocation(Enum):
    DATA_BLOCK = auto()
    EXTRA_BLOCK = auto()
    STREAM_DATA = auto()

class ControlSite:
    """Represents an individual control on the form with state flags."""
    
    # Mapping for BitFlags (Section 2.2.10.2.1.1)
    BIT_FLAG_MAP = {
        0: "Visible",
        1: "Enabled",
        2: "Locked",
        3: "FocusOnClick",
        4: "Transparent",
        5: "AutoSize",
        # Bits 6-31 are reserved or internal
    }

    CLSID_MAP = {
        0x00: "Forms.TextBox.1", 0x01: "Forms.CheckBox.1", 0x02: "Forms.OptionButton.1",
        0x03: "Forms.Label.1", 0x04: "Forms.CommandButton.1", 0x05: "Forms.ComboBox.1",
        0x06: "Forms.ListBox.1", 0x07: "Forms.ScrollBar.1", 0x08: "Forms.SpinButton.1",
        0x09: "Forms.TabStrip.1", 0x0A: "Forms.MultiPage.1", 0x0B: "Forms.Image.1",
        0x0C: "Forms.ToggleButton.1"
    }

    def __init__(self, properties: Dict[str, Any]):
        self.raw_props = properties
        self.type = self.CLSID_MAP.get(properties.get("ClsidCacheIndex", -1), "Unknown Control")
        
        # Decode BitFlags
        self.flags = {}
        raw_flags = properties.get("BitFlags", 0)
        if isinstance(raw_flags, tuple): raw_flags = raw_flags[0]
        
        for bit, label in self.BIT_FLAG_MAP.items():
            self.flags[label] = bool((raw_flags >> bit) & 1)

    def __repr__(self):
        status = "Visible" if self.flags.get("Visible") else "Hidden"
        return f"<{self.type} [{status}] ID:{self.raw_props.get('ID')}>"

class MSFormControlReader:
    # Full Property Map per Section 2.2.10.1.1
    FORM_PROP_MAP = {
        0: ("BackColor", "<I", DataLocation.DATA_BLOCK),
        1: ("ForeColor", "<I", DataLocation.DATA_BLOCK),
        2: ("NextID",    "<I", DataLocation.DATA_BLOCK),
        3: ("Left",      "<i", DataLocation.DATA_BLOCK),
        4: ("Top",       "<i", DataLocation.DATA_BLOCK),
        5: ("Width",     "<i", DataLocation.DATA_BLOCK),
        6: ("Height",    "<i", DataLocation.DATA_BLOCK),
        7: ("Caption",   "<I", DataLocation.EXTRA_BLOCK),
        8: ("Font",      "<I", DataLocation.STREAM_DATA),
        9: ("HelpID",    "<I", DataLocation.DATA_BLOCK),
        10:("MouseIcon", "<I", DataLocation.STREAM_DATA),
        11:("Pointer",   "B",   DataLocation.DATA_BLOCK),
        12:("Tag",       "<I", DataLocation.EXTRA_BLOCK),
        13:("Picture",   "<I", DataLocation.STREAM_DATA),
        14:("Zoom",      "<H", DataLocation.DATA_BLOCK),
        15:("PicAlign",  "B",   DataLocation.DATA_BLOCK),
        16:("PicTile",   "B",   DataLocation.DATA_BLOCK),
        17:("PicSize",   "B",   DataLocation.DATA_BLOCK),
        18:("Cookie",    "<I", DataLocation.DATA_BLOCK),
        19:("DrawBuf",   "<I", DataLocation.DATA_BLOCK),
        20:("BordCol",   "<I", DataLocation.DATA_BLOCK),
        21:("BordStyle", "B",   DataLocation.DATA_BLOCK),
        22:("Effect",    "B",   DataLocation.DATA_BLOCK),
        23:("FormSize",  "<I", DataLocation.DATA_BLOCK),
    }

    SITE_PROP_MAP = [
        "Name", "Tag", "ID", "HelpContextID", "BitFlags", "ObjectDepth", "TabIndex",
        "ClsidCacheIndex", "GroupsCount", "GroupsOffset", "Left", "Top", "Width", "Height",
        "ObjectStreamSize", "TabIndexProp", "Licensed", "ClsidCacheIndexProp", "ObjectStorageId",
        "ObjectStreamId", "ObjectStorageIdProp", "ObjectStreamIdProp", "IsControl", "IsStream",
        "IsStorage", "IsEmbedded", "IsContainer"
    ]

    def __init__(self, data: bytes):
        self.stream = io.BytesIO(data)
        self.properties = {}
        self.sites: List[ControlSite] = []
        self._parse()

    def _parse(self):
        # Header (Version 0.4)
        self.stream.read(2) 
        cb_form, = struct.unpack('<H', self.stream.read(2))
        prop_mask, = struct.unpack('<I', self.stream.read(4))

        extra_q, stream_q = [], []

        # 1. DataBlock
        for bit in range(24):
            if (prop_mask >> bit) & 1:
                name, fmt, loc = self.FORM_PROP_MAP[bit]
                val = struct.unpack(fmt, self.stream.read(struct.calcsize(fmt)))
                self.properties[name] = val[0] if len(val) == 1 else val
                if loc == DataLocation.EXTRA_BLOCK: extra_q.append(name)
                elif loc == DataLocation.STREAM_DATA: stream_q.append(name)

        # 2. ExtraDataBlock
        for name in extra_q:
            length, = struct.unpack('<H', self.stream.read(2))
            self.properties[f"{name}_Value"] = self.stream.read(length).decode('utf-16', errors='replace')

        # 3. StreamData (Fonts)
        for name in stream_q:
            if name == "Font":
                self.properties["Font_Details"] = self._parse_font()

        # 4. SiteData
        while True:
            mask_raw = self.stream.read(4)
            if not mask_raw or len(mask_raw) < 4: break
            site_mask, = struct.unpack('<I', mask_raw)
            if site_mask == 0: break

            site_props = {}
            for bit, s_name in enumerate(self.SITE_PROP_MAP):
                if (site_mask >> bit) & 1:
                    val, = struct.unpack('<I', self.stream.read(4))
                    site_props[s_name] = val
            self.sites.append(ControlSite(site_props))

    def _parse_font(self):
        self.stream.read(20) # Skip GUID/Ver
        name_len = ord(self.stream.read(1))
        name = self.stream.read(name_len).decode('ascii', errors='replace')
        size_raw, = struct.unpack('<Q', self.stream.read(8))
        return {"Name": name, "Size": size_raw / 10000.0}

