from ms_oforms.Models.label import Label


def test_compress() -> None:
    input = b'\xca\x05\x00\x00\xa7\x01\x00\x00'
    expected = input
    test_value = Label.compress_and_pad(input)
    assert test_value == expected


def test_mask() -> None:
    expected = b'\xf5\x01\x00\x00'
    label = Label()
    label.properties = {
        "Name": b'Label1',
        "ID": 1,
        "BitFlags": b'2\x00\x00\x00',
        "ObjectStreamSize": 0x3c,
        "TabIndex": 0,
        "ClsidCacheIndex": 0x15,
        "Position": b'\x00\x00\x00\x00\x00\x00\x00\x00'
    }
    assert label.generate_prop_mask() == expected
