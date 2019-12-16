import pytest
from secrethitlergame.phase import Phase
from unittest import mock
from secrethitlergame.voting_phase import VotingPhase


def test_initialization():
    vp = VotingPhase()
    assert isinstance(vp, Phase)
    assert vp.chancelor is None
    assert vp.president is None


def test_get_previous_government():
    player = mock.Mock()
    player.person.return_value = 'John Doe'
    vp_old = VotingPhase()
    vp_old.chancelor = player
    vp_old.president = player
    ret = vp_old.get_previous_government()
    assert all(x is None for x in ret)
    assert len(ret) == 2
    vp = VotingPhase(previous_phase=vp_old)
    ret = vp.get_previous_government()
    assert all(x is not None for x in ret)
    assert len(ret) == 2
    assert ret[0] == player


def test_add_chancelor():
    player = mock.Mock()
    player2 = mock.Mock()

    vp_old = VotingPhase()
    vp_old.add_chancelor(player)
    assert vp_old.chancelor is not None
    assert vp_old.chancelor == player

    vp = VotingPhase(previous_phase=vp_old)
    with pytest.raises(ValueError):
        vp.add_chancelor(player)
    assert vp.chancelor is None

    vp.add_chancelor(player2)
    assert vp.chancelor is not None
    assert vp.chancelor == player2


def test_add_president():
    player = mock.Mock()

    vp = VotingPhase()
    vp.add_president(player)
    assert vp.president == player


def test_failed():
    vp = VotingPhase()
    x = vp.failed()
    assert vp.next_phase == x
    assert vp != x
