import pytest
from secrethitlergame.phase import Phase


@pytest.fixture
def phase_sequence():
    return [Phase() for i in range(3)]


def test_initialization():
    p = Phase()
    assert p._previous_phase is None
    assert p._next_phase is None


def test_previous_phase_property():
    p = Phase()
    assert p._previous_phase == p.previous_phase


def test_previous_phase_setter(phase_sequence):
    new_phase = Phase()
    for i in range(1, len(phase_sequence)):
        test_phase = phase_sequence[i]
        previous_phase = phase_sequence[i - 1]
        test_phase.previous_phase = None
        assert test_phase._previous_phase is None

        test_phase.previous_phase = previous_phase
        assert test_phase.previous_phase == previous_phase

        test_phase.previous_phase = previous_phase
        assert test_phase.previous_phase == previous_phase

        test_phase.previous_phase = new_phase
        assert test_phase.previous_phase == new_phase
        assert new_phase.next_phase == test_phase


def test_next_phase_property():
    p = Phase()
    assert p._next_phase == p.next_phase


def test_next_phase_setter(phase_sequence):
    new_phase = Phase()
    for i in range(len(phase_sequence) - 1):
        test_phase = phase_sequence[i]
        next_phase = phase_sequence[i + 1]

        test_phase.next_phase = None
        assert test_phase._next_phase is None

        test_phase.next_phase = next_phase
        assert test_phase.next_phase == next_phase

        test_phase.next_phase = next_phase
        assert test_phase.next_phase == next_phase

        test_phase.next_phase = new_phase
        assert test_phase.next_phase == new_phase
        assert new_phase.previous_phase == test_phase


def test_next_phase_deleter():
    p = Phase()
    del p.next_phase
    assert hasattr(p, '_next_phase')
    assert p._next_phase is None


def test_remove(phase_sequence):
    for i in range(len(phase_sequence) - 1):
        p = phase_sequence[i]
        p_next = phase_sequence[i + 1]
        p.next_phase = p_next

    phase_sequence[0].remove()
    assert phase_sequence[1].previous_phase is None
    phase_sequence[1].previous_phase = phase_sequence[0]

    phase_sequence[1].remove()
    assert phase_sequence[0].next_phase != phase_sequence[1]
    assert phase_sequence[0].next_phase is not None
    assert phase_sequence[0].next_phase == phase_sequence[2]

    assert phase_sequence[2].previous_phase != phase_sequence[1]
    assert phase_sequence[2].previous_phase is not None
    assert phase_sequence[2].previous_phase == phase_sequence[0]

    phase_sequence[0].next_phase = phase_sequence[1]

    phase_sequence[2].remove()
    print(phase_sequence[1].next_phase)
    # assert phase_sequence[1].next_phase is None


def test_is_first(phase_sequence):
    for i in range(len(phase_sequence) - 1):
        p = phase_sequence[i]
        p_next = phase_sequence[i + 1]
        p.next_phase = p_next

    assert phase_sequence[0].is_first()
    assert not phase_sequence[1].is_first()
    assert not phase_sequence[2].is_first()


def test_is_last(phase_sequence):
    for i in range(len(phase_sequence) - 1):
        p = phase_sequence[i]
        p_next = phase_sequence[i + 1]
        p.next_phase = p_next

    assert not phase_sequence[0].is_last()
    assert not phase_sequence[1].is_last()
    assert phase_sequence[2].is_last()


def test_is_isolated(phase_sequence):
    for p in phase_sequence:
        assert p.is_isolated()

    for i in range(len(phase_sequence) - 1):
        p = phase_sequence[i]
        p_next = phase_sequence[i + 1]
        p.next_phase = p_next

    for p in phase_sequence:
        assert not p.is_isolated()
