from ms_oforms.Models.label import Label


def test_compress() -> None:
    label = Label()
    input = b'Label1'
    expected = b'Label1\x00\x00'
    test_value = Label.compress_and_pad(input)
    assert test_value == expected
