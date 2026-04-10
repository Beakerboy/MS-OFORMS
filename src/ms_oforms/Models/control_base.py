import struct
from typing import TypeVar


T = TypeVar('T', bound='ControlBase')


class ControlBase:

    def generate_prop_mask(self: T) -> int:
        """
        Recreates a 4-byte PropMask bitfield based on a dictionary of properties.
        """
        mask = 0
    
        # Iterate through the known mapping for this object type
        for bit, map_data in self.PROP_MAP.items():
            # Get the property name from the map (usually the first element)
            prop_name = map_data[0]
        
            # If the property exists in the dict and is not None, set the bit
            if prop_name in self.properties and self.properties[prop_name] is not None:
                mask |= (1 << bit)
            
        return mask 

    def to_bytes(self: T) -> bytes:
        data = b''
        extra = b''
        for bit, map_data in self.PROP_MAP.items():
                name = map_data[0]
                if name in self.properties:
                    value = self.properties[name]
                    if map_data[2] == DataLocation.BOTH:
                        cba = len(value) | 0x80000000
                        data += struct.pack("<I", cba)
                        extra += self.compress_and_pad(value)
                    elif map_data[2] == DataLocation.DATA_BLOCK:
                        if map_data[1] == "s":
                            data += value
                        else:
                            data += struct.pack(map_data[1], value)
                    elif map_data[2] == DataLocation.EXTRA_BLOCK:
                        extra += self.compress_and_pad(value)
        cb_label = 4 + len(data) + len(extra)
        prop_mask = self.generate_prop_mask()
        return (
            struct.pack('<BBHI', 0, 2, cb_label, prop_mask) +
            data + extra
        )

    @staticmethod
    def compress_and_pad(value: bytes) -> bytes:
        # if all the high bits are zero, remove them
        # pad to 4 byte length
        pad = b''
        if len(value) % 4 > 0:
            pad = b'\x00' * (4 - len(value) % 4)
        return value + pad
