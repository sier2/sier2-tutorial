import tutorial_0a
import pytest

# Test different ways of running the AddOne block.

def test_3plus1_param():
    b = tutorial_0a.AddOne()
    b.in_a = 3
    b.execute()

    assert b.out_a == 4

def test_3plus1_call():
    b = tutorial_0a.AddOne()
    r = b(in_a=3)

    assert r['out_a'] == 4

def test_3plus1_kwargs():
    b = tutorial_0a.AddOne()
    kwargs = {'in_a': 3}
    r = b(**kwargs)

    assert r['out_a'] == 4

# Test different ways of running the UpperCase block.
#

def test_upper_param():
    b = tutorial_0a.SingleCase()
    b.in_str = 'Some text.'
    b.in_upper = True
    b.execute()

    assert b.out_str == 'SOME TEXT.'

def test_upper_call():
    b = tutorial_0a.SingleCase()
    r = b(in_str='Some text.', in_upper=False)

    assert r['out_str'] == 'some text.'

def test_bad_int():
    """An integer param can't be a string."""

    b = tutorial_0a.AddOne()

    with pytest.raises(ValueError):
        r = b(in_a='three')
