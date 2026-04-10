from ms_cfb.ole_file import OleFile
from ms_oforms.Models.form_embedded import FormEmbedded
from ms_oforms.Models.label import Label
from ms_oforms.Models.morph_data import MorphData


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
    label1 = Label()
    label1.properties = {
        "Caption": b'User Name',
        "Size": b'\xca\x05\x00\x00\xa7\x01\x00\x00',
        "FontName": b'Tahoma',
        "FontHeight": 0xa5,
        "FontCharset": 0x00,
        "FontPitchAndFamily": 0x02
    }
    
    textbox = MorphData()
    textbox.properties = {
        "Various": b'\x1bH\x80,',
        "Size": b'\xb6\x0f\x00\x00\x7b\x02\x00\x00',
        "FontName": b'Tahoma',
        "FontHeight": 0xa5,
        "FontCharset": 0x00,
        "FontPitchAndFamily": 0x02
    }

    label2 = Label()
    label2.properties = {
        "Caption": b'Password',
        "Size": b'\xf6\x04\x00\x00\xa7\x01\x00\x00',
        "FontName": b'Tahoma',
        "FontHeight": 0xa5,
        "FontCharset": 0x00,
        "FontPitchAndFamily": 0x02
    }
    form.objects = [label1, textbox, label2]
    
    assert form.to_bytes() == expected
