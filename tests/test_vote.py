import pytest
from secrethitlergame.vote import Vote


def test_initialization():
    v = Vote()
    assert v._value is None
    assert v._possible_votes == ['Ja', 'Nein', None]


def test_upvote():
    v = Vote()
    v.upvote()
    assert v.value == 'Ja'


def test_downvote():
    v = Vote()
    v.downvote()
    assert v.value == 'Nein'


def test_value_getter():
    v = Vote()
    assert v.value is None
    assert v.value == v._value
    v.upvote()
    assert v.value == 'Ja'
    assert v.value == v._value
    v.downvote()
    assert v.value == 'Nein'
    assert v.value == v._value


def test_value_setter():
    v = Vote()
    v.value = 'Ja'
    assert v._value == 'Ja'
    v.value = 'Nein'
    assert v._value == 'Nein'
    with pytest.raises(ValueError):
        v.value = 'This is not something you can vote'
    assert v._value == 'Nein'
    v.value = None
    assert v._value is None


def test_value_deleter():
    v = Vote()
    v.value = 'Ja'
    del v.value
    assert v.value == 'Ja'
    assert v._value == 'Ja'


def test_is_approval():
    v = Vote()
    v.upvote()
    assert v.is_approval()
    v.value = 'Ja'
    assert v.is_approval()


def test_is_disapproval():
    v = Vote()
    v.downvote()
    assert v.is_disapproval()
    v.value = 'Nein'
    assert v.is_disapproval()


def test_is_none():
    v = Vote()
    assert v.is_none()
    v.value = None
    assert v.is_none()
    v._value = None
    assert v.is_none()
