from arithmetic_logic_unit import alu


def test_negation():
    assert alu.negation(7) == -7
    assert alu.negation(-100) == 100


def test_check_3x_equal():
    assert alu.check_3x_equal(4, 7) == False
    assert alu.check_3x_equal(3, 9) == True


def test_binary():
    assert alu.binary(1) == '0001'
    assert alu.binary(127) == '1111'
    assert alu.binary(256) == '0000'

def test_monad():
    assert alu.monad(13579246899999) == False