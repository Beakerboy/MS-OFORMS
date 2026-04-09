from ms_cfb.ole_file import OleFile
from ms_oforms.Models.form_control import FormControl


def test_generate_flags() -> None:
    form = FormControl()
    form.properties["NextID"] = 5
    form.properties["Display"] = 0x0d3b00000fd0
    form.properties["LogicalSize"] = 0
    form.properties["ShapeCookie"] = 8
    form.properties["DrawBuffer"] = 0x7d00
    expected = 0x0c000c08
    assert form.generate_prop_mask() == expected


def test_generate_data() -> None:
    form = FormControl()
    form.properties["NextID"] = 5
    form.properties["Display"] = 0x0d3b00000fd0
    form.properties["LogicalSize"] = 0
    form.properties["ShapeCookie"] = 8
    form.properties["DrawBuffer"] = 0x7d00
    expected = b'\x05\x00\x00\x00\x08\x00\x00\x00\x00}\x00\x00'
    assert form.generate_data_block() == expected


def test_generate_extra() -> None:
    form = FormControl()
    form.properties["NextID"] = 5
    form.properties["Display"] = 0x0d3b00000fd0
    form.properties["LogicalSize"] = 0
    form.properties["ShapeCookie"] = 8
    form.properties["DrawBuffer"] = 0x7d00
    expected = b'\xd0\x0f\x00\x00;\x0d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    assert form.generate_extra_data_block() == expected


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
    form = FormControl()
    form.properties["NextID"] = 5
    form.properties["Display"] = 0x0d3b00000fd0
    form.properties["LogicalSize"] = 0
    form.properties["ShapeCookie"] = 8
    form.properties["DrawBuffer"] = 0x7d00
    site1_data = {
        "Name": b'\x00\x00\x06\x00',
        "ID": b'\x00\x80\x01\x00',
        "BitFlags": b'\x00\x002\x00',
        "ObjectStreamSize": b'\x00\x00\x00\x00',
        "TabIndex": b'\x00\x00',
        "ClsidCacheIndex": b'\x00\x00',
        "GroupId": b'\x00\x00'
    }
    site1_extra = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    form.sites = [
        (0x01f5, site1_data, site1_extra), (0, site1_data, b''), (0, site1_data, b''),
        (0, site1_data, b''), (0, site1_data, b'')
    ]
    form.depth = b'\x00\x85\x01'  # 5 consecutive ssites with type 1 depth 0
    assert form.to_bytes() == expected
