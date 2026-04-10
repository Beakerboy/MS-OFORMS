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
        "Size": b'\xca\x05\x00\x00\xa7\x01\x00\x00'
    }
    label1.text_props.properties = {
        "FontName": b'Tahoma',
        "FontHeight": 0xa5,
        "FontCharset": 0x00,
        "FontPitchAndFamily": 0x02
    }
    
    textbox = MorphData()
    textbox.properties["Various"] = b'\x1bH\x80,'
    textbox.properties["Size"] = b'\x00\x01\x02\x03\x04\x05\x06\c07'
    form.objects = [label1, textbox]
    
    assert form.to_bytes() == expected
