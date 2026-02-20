from codes import to_direct, to_invert, to_additional


def test_direct():
    assert to_direct(11, 8) == "00001011"
    assert to_direct(-11, 8) == "10001011"
    assert to_direct(-21, 8) == "10010101"


def test_invert():
    assert to_invert(21, 8) == "00010101"
    assert to_invert(-11, 8) == "11110100"
    assert to_invert(-21, 8) == "11101010"


def test_additional():
    assert to_additional(-22, 8) == "11101010"
    assert to_additional(21, 8) == "00010101"
