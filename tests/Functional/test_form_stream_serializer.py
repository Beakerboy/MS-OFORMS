from ms_cfb.ole_file import OleFile
from ms_oforms.Views.form_stream_serializer import FormStreamSerializer


def test_generate_flags() -> None:
    properties = {
        "NextID": 5,
        "Display": 0x0d3b00000fd0,
        "LogicalSize": 0,
        "ShapeCookie": 8,
        "DrawBuffer": 0x7d00
    }
    stream = FormStreamSerializer(properties)
    expected = 0x0c000c08
    assert stream.generate_prop_mask() == expected


def test_generate_data() -> None:
    properties = {
        "NextID": 5,
        "Display": 0x0d3b00000fd0,
        "LogicalSize": 0,
        "ShapeCookie": 8,
        "DrawBuffer": 0x7d00
    }
    stream = FormStreamSerializer(properties)
    expected = b'\x05\x00\x00\x00\x08\x00\x00\x00\x00}\x00\x00'
    assert stream.generate_data_block() == expected


def test_generate_extra() -> None:
    properties = {
        "NextID": 5,
        "Display": 0x0d3b00000fd0,
        "LogicalSize": 0,
        "ShapeCookie": 8,
        "DrawBuffer": 0x7d00
    }
    stream = FormStreamSerializer(properties)
    expected = b'\xd0\x0f\x00\x00;\x0d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    assert stream.generate_extra_data_block() == expected


def test_to_bytes() -> None:
    path1 = 'tests/files/Login.frx'
    path2 = 'tests/files/Login.bin'
    path3 = 'tests/files/f.bin'
    with open(path1, 'rb') as file:
        file.read(24)
        ole_data = file.read()
    with open(path2, 'wb') as file:
        file.write(ole_data)
    with open(path2, 'rb') as file:
        olefile = OleFile.create_from_file(path2)
        olefile.extract_stream('f', 'tests/files')
    with open(path3, 'rb') as file:
        expected = file.read()
    
    properties = {
        "NextID": 5,
        "Display": 0x0d3b00000fd0,
        "LogicalSize": 0,
        "ShapeCookie": 8,
        "DrawBuffer": 0x7d00
    }
    serializer = FormStreamSerializer(properties)
    site1_mask = b'\xf5\x01\x00\x00'
    site1_data = {
        "Name": b'Label1',
        "ID": 1,
        "BitFlags": b'2\x00\x00\x00',
        "ObjectStreamSize": 0x3c,
        "TabIndex": 0,
        "ClsidCacheIndex": 0x15,
        "Position": b'\x00\x00\x00\x00\x00\x00\x00\x00'
    }
    site2_data = {
        "Name": b'Username',
        "ID": 2,
        "ObjectStreamSize": 0x34,
        "TabIndex": 1,
        "ClsidCacheIndex": 0x17,
        "Position": b'\x00\x00\x00\x00\xa7\x01\x00\x00'
    }
    site2_mask = b'\xe5\x01\x00\x00'
    site3_mask = b'\xf5\x01\x00\x00'
    site3_data = {
        "Name": b'Label2',
        "ID": 3,
        "BitFlags": b'2\x00\x00\x00',
        "ObjectStreamSize": 0x38,
        "TabIndex": 2,
        "ClsidCacheIndex": 0x15,
        "Position": b'\x00\x00\x00\x00\xf6\x04\x00\x00'
    }
    site4_mask = b'\xe5\x01\x00\x00'
    site4_data = {
        "Name": b'Password',
        "ID": 4,
        "ObjectStreamSize": 0x38,
        "TabIndex": 3,
        "ClsidCacheIndex": 0x17,
        "Position": b'\x00\x00\x00\x00\x9d\x06\x00\x00'
    }
    site5_mask = b'\xe5\x01\x00\x00'
    site5_data = {
        "Name": b'LoginButton',
        "ID": 5,
        "ObjectStreamSize": 0x38,
        "TabIndex": 4,
        "ClsidCacheIndex": 0x11,
        "Position": b'\x1f\x00\x00\x00\x00\xec\x09\x00'
    }
    serializer.sites = [
        site1_data, site2_data, site3_data,
        site4_data, site5_data
    ]
    serializer.depth = b'\x00\x85\x01'  # 5 consecutive ssites with type 1 depth 0
    assert serializer.to_bytes() == expected
