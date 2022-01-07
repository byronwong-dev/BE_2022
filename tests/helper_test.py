from helpers.ratio import is_diminishing_ratio, get_diminishing_amounts
from fractions import Fraction

def test_is_diminishing_ratio():

    assert is_diminishing_ratio(2.50, 10000) is True
    assert is_diminishing_ratio(100, 100) is False
    assert is_diminishing_ratio(1, 1000) is True
    assert is_diminishing_ratio(1, 999) is True
    assert is_diminishing_ratio(1, 99) is False
    assert is_diminishing_ratio(1, 1) is False
    assert is_diminishing_ratio(0.5, 99) is True
    assert is_diminishing_ratio(Fraction(1,99)) is False

def test_can_detect_diminishing_ratio():
    assert get_diminishing_amounts([2.50, 10000, 500]) == [2.50]
    assert get_diminishing_amounts([200, 10000, 500]) is None
    assert get_diminishing_amounts([100, 100, 100]) is None
    assert get_diminishing_amounts([9991, 990, 10]) == [10]
    assert get_diminishing_amounts([9991, 1000, 10]) == [10]
    assert get_diminishing_amounts([10000, 10, 2]) == [10, 2]