from ms_oforms.Models.label import Label


def test_compress() -> None:
    input = b'\xca\x05\x00\x00\xa7\x01\x00\x00'
    expected = input
    test_value = Label.compress_and_pad(input)
    assert len(test_value) == 8
