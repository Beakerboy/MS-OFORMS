from ms_cfb.ole_file import OleFile
from ms_oforms.Models.form_embedded import FormEmbedded
from ms_oforms.Models.label import Label

def test_to_bytes() -> None:
    path1 = 'tests/files/Login.frx'
    path2 = 'tests/files/Login.bin'
    path3 = 'tests/files/o.bin'
    with open(path1, 'rb') as file:
        file.read(24)
        ole_data = file.read()
    with open(path2, 'wb') as file:
        file.write(ole_data)
    with open(path2, 'rb') as file:
        olefile = OleFile.create_from_file(path2)
        olefile.extract_stream('o', 'tests/files')
    with open(path3, 'rb') as file:
        expected = file.read()
    form = FormEmbedded()
    label = Label()
    label.properties = {
        "Caption": b'',
        "Size": 0
    }
    form.objects = [Label()]
    
    assert form.to_bytes() == expected
