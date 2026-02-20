from operations import operations_direct, operations_additional,\
    operations_inverted, multiply_direct, multiply_additional


def test_add_direct():
    assert operations_direct(11, 21, 8) == "00100000"
    assert operations_direct(11, -21, 8) == "10001010"
    assert operations_direct(-11, 21, 8) == "00001010"
    assert operations_direct(-11, -21, 8) == "10100000"


def test_add_additional():
    assert operations_additional(11, 21, 8) == "00100000"
    assert operations_additional(11, -21, 8) == "11110110"
    assert operations_additional(-11, 21, 8) == "00001010"
    assert operations_additional(-11, -21, 8) == "11100000"


def test_add_inverted():
    assert operations_inverted(11, 21, 8) == "00100000"
    assert operations_inverted(11, -21, 8) == "11110101"
    assert operations_inverted(-11, 21, 8) == "00001010"
    assert operations_inverted(-11, -21, 8) == "11011111"


def test_multiply_direct():
    assert multiply_direct(11, 21, 8) == "011100111"
    assert multiply_direct(11, -21, 8) == "111100111"
    assert multiply_direct(-11, 21, 8) == "111100111"
    assert multiply_direct(-11, -21, 8) == "011100111"


def test_multiply_additional():
    assert multiply_additional(11, 21, 8) == "011100111"
    assert multiply_additional(11, -21, 8) == "100011001"
    assert multiply_additional(-11, 21, 8) == "100011001"
    assert multiply_additional(-11, -21, 8) == "011100111"

