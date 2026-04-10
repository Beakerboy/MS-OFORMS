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
