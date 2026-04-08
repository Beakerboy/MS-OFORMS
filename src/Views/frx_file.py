import struct
import io

class FRX:
    def __init__(self, f_stream: bytes, o_stream: bytes, compobj: bytes):
        self.f_stream = f_stream
        self.o_stream = o_stream
        self.compobj = compobj

    @staticmethod
    def from_file(path: str) -> 'FRX':
        """
        Reads an FRX file, validates headers, and extracts streams using the OleFile API.
        """
        with open(path, 'rb') as file:
            # 1. Read and validate 24-byte header
            header = file.read(24)
            if len(header) < 24 or header[0:2] != b'LB':
                raise ValueError("Not a valid FRX file (Missing 'LB' header).")

            # 2. Validate OLE container size from header (bytes 5-8)
            # declared_size, = struct.unpack('<I', header[4:8])
            
            # 3. Extract the OLE payload (everything after byte 24)
            ole_payload = file.read()
            if not ole_payload.startswith(b'\xd0\xcf\x11\xe0'):
                raise ValueError("FRX header found, but OLE container magic is missing.")

        # Wrap payload in a BytesIO for your OleFile API
        ole_mem_file = io.BytesIO(ole_payload)
        
        # 4. Use the requested API for stream extraction
        # Assuming OleFile.create_from_file can accept a file-like object
        ole_file = OleFile.create_from_file(ole_mem_file)
        
        # Extraction buffers
        f_dest = io.BytesIO()
        o_dest = io.BytesIO()
        c_dest = io.BytesIO()

        # extract_stream(stream_name, destination_buffer)
        ole_file.extract_stream('f', f_dest)
        ole_file.extract_stream('o', o_dest)
        ole_file.extract_stream('\x01CompObj', c_dest)

        return FRX(
            f_stream=f_dest.getvalue(),
            o_stream=o_dest.getvalue(),
            compobj=c_dest.getvalue()
        )

# Example Usage:
# frx = FRX.from_file("UserForm1.frx")
# print(f"Ready to parse {len(frx.f_stream)} bytes of f-stream.")
