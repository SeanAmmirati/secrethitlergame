import pytest
from secrethitlergame.government import Government
from secrethitlergame.vote import Vote


@pytest.fixture
def yes_vote():
    v = Vote()
    v.upvote()
    return v


@pytest.fixture
def no_vote():
    v = Vote()
    v.downvote()
    return v


def test_initialization():
    g = Government()
    assert g.chancelor is None
    assert g.president is None
    assert not g.approved
    assert not g.votes


def test_add_chancelor():
    g = Government()
    g.add_chancelor(1)
    assert g.chancelor == 1

    g = Government()
    g.add_president(1)
    with pytest.raises(ValueError):
        g.add_chancelor(1)


def test_add_president():
    g = Government()
    g.add_president(1)
    assert g.president == 1

    g = Government()
    g.add_chancelor(1)
    with pytest.raises(ValueError):
        g.add_president(1)


def test_remove_president():
    g = Government()
    g.add_president(1)
    g.remove_president()
    assert g.president is None


def test_remove_chancelor():
    g = Government()
    g.add_chancelor(1)
    g.remove_chancelor()
    assert g.chancelor is None


def test_add_vote(yes_vote, no_vote):
    # Case 1 -- no chancellor or president
    g = Government()
    with pytest.raises(NotImplementedError):
        g.add_vote(yes_vote)

    # Case 2 -- only chancelor
    g.add_chancelor(1)

    with pytest.raises(NotImplementedError):
        g.add_vote(yes_vote)

    # Case 3 -- only president
    g.remove_chancelor()
    g.add_president(2)
    with pytest.raises(NotImplementedError):
        g.add_vote(yes_vote)

    # Case 4 both

    g.add_chancelor(1)
    g.add_vote(yes_vote)
    assert g.votes == [yes_vote]

    g.add_vote(no_vote)
    assert g.votes == [yes_vote, no_vote]

    g.add_chancelor(1)
    g.add_president(2)

    with pytest.raises(TypeError):
        g.add_vote('Ja')


def test_add_votes(yes_vote, no_vote):
    votes = [yes_vote, no_vote]
    g = Government()
    g.add_chancelor(1)
    g.add_president(2)
    g.add_votes(votes)
    assert g.votes == votes


def test_reset_votes(yes_vote):
    g = Government()
    g.add_chancelor(1)
    g.add_president(2)
    assert g.reset_votes() is None

    g.add_vote(yes_vote)
    g.reset_votes()
    assert not g.votes


def test_passed(yes_vote, no_vote):
    unanimous_pass = [yes_vote] * 4
    clear_pass = [yes_vote] * 3 + [no_vote]
    even_split = [yes_vote] * 2 + [no_vote] * 2
    clear_fail = [yes_vote] * 1 + [no_vote] * 3
    unanimous_fail = [no_vote] * 4

    g = Government()

    g.add_chancelor(1)
    g.add_president(2)

    g.add_votes(unanimous_pass)
    assert g.passed()
    g.reset_votes()

    g.add_votes(clear_pass)
    assert g.passed()
    g.reset_votes()

    g.add_votes(even_split)
    assert not g.passed()
    g.reset_votes()

    g.add_votes(clear_fail)
    assert not g.passed()
    g.reset_votes()

    g.add_votes(unanimous_fail)
    assert not g.passed()
    g.reset_votes()


def test_failed(yes_vote, no_vote):
    unanimous_pass = [yes_vote] * 4
    clear_pass = [yes_vote] * 3 + [no_vote]
    even_split = [yes_vote] * 2 + [no_vote] * 2
    clear_fail = [yes_vote] * 1 + [no_vote] * 3
    unanimous_fail = [no_vote] * 4

    g = Government()

    g.add_chancelor(1)
    g.add_president(2)

    g.add_votes(unanimous_pass)
    assert not g.failed()
    g.reset_votes()

    g.add_votes(clear_pass)
    assert not g.failed()
    g.reset_votes()

    g.add_votes(even_split)
    assert g.failed()
    g.reset_votes()

    g.add_votes(clear_fail)
    assert g.failed()
    g.reset_votes()

    g.add_votes(unanimous_fail)
    assert g.failed()
    g.reset_votes()
