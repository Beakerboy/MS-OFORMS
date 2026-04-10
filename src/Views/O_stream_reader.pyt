import struct
import io
from enum import Enum, auto
from typing import Dict, List, Any, Optional, Type

# --- Enums and Data Descriptors ---

class DataLocation(Enum):
    DATA_BLOCK = auto()
    EXTRA_BLOCK = auto()
    STREAM_DATA = auto()

class FontDescriptor:
    def __init__(self, name: str, size: float, weight: int):
        self.name = name
        self.size = size
        self.weight = weight

    def __repr__(self):
        return f"<Font: {self.name} {self.size}pt>"

# --- Control Data Parsers ('o' Stream Logic) ---

class BaseControlData:
    """Base class for control-specific data in the 'o' stream."""
    def __init__(self, stream: io.BytesIO):
        self.properties = {}
        self.stream = stream
        self.parse()

    def read_extra_string(self):
        try:
            length, = struct.unpack('<I', self.stream.read(4))
            return self.stream.read(length).decode('utf-16', errors='replace')
        except: return ""

    def parse(self): pass

class TextBoxData(BaseControlData):
    def parse(self):
        mask, = struct.unpack('<I', self.stream.read(4))
        if mask & (1 << 0): self.properties['Value'] = self.read_extra_string()
        if mask & (1 << 1): self.properties['MaxLength'], = struct.unpack('<I', self.stream.read(4))

class CheckBoxData(BaseControlData):
    def parse(self):
        mask, = struct.unpack('<I', self.stream.read(4))
        if mask & (1 << 0):
            val, = struct.unpack('<i', self.stream.read(4))
            self.properties['Value'] = True if val == -1 else False
        if mask & (1 << 1): self.properties['Caption'] = self.read_extra_string()

class ListBoxData(BaseControlData):
    def parse(self):
        mask, = struct.unpack('<I', self.stream.read(4))
        if mask & (1 << 0): self.properties['Value'] = self.read_extra_string()
        if mask & (1 << 2): self.properties['ColumnCount'], = struct.unpack('<I', self.stream.read(4))

class MultiPageData(BaseControlData):
    def parse(self):
        mask, = struct.unpack('<I', self.stream.read(4))
        if mask & (1 << 0): self.properties['ActivePage'], = struct.unpack('<I', self.stream.read(4))
        if mask & (1 << 3): self.properties['PageCount'], = struct.unpack('<I', self.stream.read(4))

class ControlDataFactory:
    TYPE_MAP = {
        "Forms.TextBox.1": TextBoxData,
        "Forms.Label.1": TextBoxData,
        "Forms.ComboBox.1": ListBoxData,
        "Forms.ListBox.1": ListBoxData,
        "Forms.CheckBox.1": CheckBoxData,
        "Forms.OptionButton.1": CheckBoxData,
        "Forms.CommandButton.1": TextBoxData, # Caption is usually Bit 0
        "Forms.MultiPage.1": MultiPageData,
    }

    @classmethod
    def create(cls, control_type: str, stream: io.BytesIO) -> Optional[BaseControlData]:
        parser_cls = cls.TYPE_MAP.get(control_type, BaseControlData)
        return parser_cls(stream)

# --- Site and Form Parser ('f' Stream Logic) ---

class ControlSite:
    BIT_FLAG_MAP = {0: "Visible", 1: "Enabled", 2: "Locked", 4: "Transparent"}
    CLSID_MAP = {
        0x0: "Forms.TextBox.1", 0x1: "Forms.CheckBox.1", 0x2: "Forms.OptionButton.1",
        0x3: "Forms.Label.1", 0x4: "Forms.CommandButton.1", 0x5: "Forms.ComboBox.1",
        0x6: "Forms.ListBox.1", 0xA: "Forms.MultiPage.1"
    }

    def __init__(self, props: Dict):
        self.id = props.get("ID")
        self.type = self.CLSID_MAP.get(props.get("ClsidCacheIndex", -1), "Unknown")
        self.flags = {label: bool((props.get("BitFlags", 0) >> bit) & 1) 
                      for bit, label in self.BIT_FLAG_MAP.items()}
        self.geometry = {"top": props.get("Top", 0)/15, "left": props.get("Left", 0)/15}

class MSOFormsParser:
    FORM_PROP_MAP = {
        0: ("BackColor", "<I", DataLocation.DATA_BLOCK), 1: ("ForeColor", "<I", DataLocation.DATA_BLOCK),
        3: ("Left",      "<i", DataLocation.DATA_BLOCK), 4: ("Top",       "<i", DataLocation.DATA_BLOCK),
        5: ("Width",     "<i", DataLocation.DATA_BLOCK), 6: ("Height",    "<i", DataLocation.DATA_BLOCK),
        7: ("Caption",   "<I", DataLocation.EXTRA_BLOCK),8: ("Font",      "<I", DataLocation.STREAM_DATA),
        12:("Tag",       "<I", DataLocation.EXTRA_BLOCK),14:("Zoom",      "<H", DataLocation.DATA_BLOCK),
        23:("FormSize",  "<I", DataLocation.DATA_BLOCK),
    }

    SITE_PROPS = ["Name", "Tag", "ID", "HelpID", "BitFlags", "Depth", "TabIndex", "ClsidCacheIndex"]

    def __init__(self, f_data: bytes, o_data: bytes = None):
        self.f_stream = io.BytesIO(f_data)
        self.form_properties = {}
        self.sites: List[ControlSite] = []
        self._parse_f_stream()
        
        self.control_values = {}
        if o_data:
            self._parse_o_stream(o_data)

    def _parse_f_stream(self):
        self.f_stream.read(2) # Version
        cb_form, = struct.unpack('<H', self.f_stream.read(2))
        prop_mask, = struct.unpack('<I', self.f_stream.read(4))

        extra_q, stream_q = [], []
        for bit, (name, fmt, loc) in self.FORM_PROP_MAP.items():
            if (prop_mask >> bit) & 1:
                val = struct.unpack(fmt, self.f_stream.read(struct.calcsize(fmt)))
                self.form_properties[name] = val[0]
                if loc == DataLocation.EXTRA_BLOCK: extra_q.append(name)
                elif loc == DataLocation.STREAM_DATA: stream_q.append(name)

        for name in extra_q:
            length, = struct.unpack('<H', self.f_stream.read(2))
            self.form_properties[name] = self.f_stream.read(length).decode('utf-16')

        while True:
            mask_raw = self.f_stream.read(4)
            if not mask_raw or len(mask_raw) < 4: break
            site_mask, = struct.unpack('<I', mask_raw)
            if site_mask == 0: break
            
            s_props = {}
            for bit, name in enumerate(self.SITE_PROPS):
                if (site_mask >> bit) & 1:
                    s_props[name], = struct.unpack('<I', self.f_stream.read(4))
            self.sites.append(ControlSite(s_props))

    def _parse_o_stream(self, o_data: bytes):
        o_stream = io.BytesIO(o_data)
        for site in self.sites:
            data_obj = ControlDataFactory.create(site.type, o_stream)
            if data_obj:
                self.control_values[site.id] = data_obj.properties

# --- Implementation Example ---
# parser = MSOFormsParser(f_bytes, o_bytes)
# for site in parser.sites:
#     val = parser.control_values.get(site.id, {}).get("Value", "N/A")
#     print(f"{site.type} (ID:{site.id}): {val}")
