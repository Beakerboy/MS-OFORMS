from ms_cfb.ole_file import OleFile
from ms_oforms.Models.form_control import FormControl


def test_generate_flags() -> None;
    form = FormControl()
    form.properties["NextID"] = 5
    form.properties["LogicalSize"] = 5
    expected = 0x0c000c08
    assert form.generate_prop_mask() == expected


def tests_to_bytes() -> None:
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
        expected = file.read
    form = FormControl()
    assert form.to_bytes() == expected
