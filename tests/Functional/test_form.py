from ms_oforms.form import Form
from ms_oforms.Models.command_button import CommandButton
from ms_oforms.Models.label import Label
from ms_oforms.Models.morph_data import MorphData


# A handful of padding bytes are incorrect
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
    form = Form()
    font_info = {
        "FontName": b'Tahoma',
        "FontHeight": 0xa5,
        "FontCharset": 0x00,
        "FontPitchAndFamily": 0x02,
    }

    label1 = Label()
    label1.properties = {
        "Caption": b'User Name',
        "Size": b'\xca\x05\x00\x00\xa7\x01\x00\x00',
        "Name": b'Label1',
        "BitFlags": b'2\x00\x00\x00',
        "ObjectStreamSize": 0x3c,
        "TabIndex": 0,
        "ClsidCacheIndex": 0x15,
        "Position": b'\x00\x00\x00\x00\x00\x00\x00\x00'
    } | font_info
    
    textbox1 = MorphData()
    textbox1.properties = {
        "Various": b'\x1bH\x80,',
        "Size": b'\xb6\x0f\x00\x00\x7b\x02\x00\x00',
        "Name": b'Username',
        "ObjectStreamSize": 0x34,
        "ClsidCacheIndex": 0x17,
        "Position": b'\x00\x00\x00\x00\xa7\x01\x00\x00'
    } | font_info

    label2 = Label()
    label2.properties = {
        "Caption": b'Password',
        "Size": b'\xf6\x04\x00\x00\xa7\x01\x00\x00',
        "Name": b'Label2',
        "BitFlags": b'2\x00\x00\x00',
        "ObjectStreamSize": 0x38,
        "ClsidCacheIndex": 0x15,
        "Position": b'\x00\x00\x00\x00\x00\x00\xf6\x04'
    } | font_info

    textbox2 = MorphData()
    textbox2.properties = {
        "Various": b'\x1bH\x80,',
        "Size": b'\xb6\x0f\x00\x00\x7b\x02\x00\x00',
        "PasswordChar": 0x2a,
        "Name": b'Password',
        "ObjectStreamSize": 0x38,
        "ClsidCacheIndex": 0x17,
        "Position": b'\x00\x00\x00\x00\x9d\x06\x00\x00'
    } | font_info

    command = CommandButton()
    command.properties = {
        "Caption": b'Log In',
        "Size": b'\xb6\x0f\x00\x00O\x03\x00\x00',
        "ParagraphAlign": 3,
        "Name": b'LoginButton',
        "ObjectStreamSize": 0x38,
        "ClsidCacheIndex": 0x11,
        "Position": b'\x1f\x00\x00\x00\x00\xec\x09\x00'
    } | font_info
    
    form.add_control(label1))
    form.add_control(textbox1)
    form.add_control(label2)
    form.add_control(textbox2)
    form.add_control(command)
    
    form.write_frx()
