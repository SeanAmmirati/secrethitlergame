import pytest

from secrethitlergame.special_phase import SpecialPhase, ExecutionPhase, ChooseNextPresidentPhase, PeekDeckPhase, PeekPlayerPhase
from secrethitlergame.enactment_phase import EnactmentPhase
from secrethitlergame.phase import Phase
from secrethitlergame.cards import DrawDeck

from unittest.mock import Mock


class TestSpecialPhase:

    def test_initialization(self):
        sp = SpecialPhase()
        assert isinstance(sp, Phase)
        assert sp.player is None

    def test_find_last_president(self):
        sp = SpecialPhase()
        enactment_phase = EnactmentPhase()
        player = Mock()
        enactment_phase.president = player
        with pytest.raises(NotImplementedError):
            sp.find_last_president()
        sp.previous_phase = enactment_phase
        sp.find_last_president()
        assert sp.player == player

    def test_action(self):
        sp = SpecialPhase()
        assert sp.action() is None


class TestExecutionPhase:

    def test_execute_player(self):
        player = Mock()
        player.alive = True
        player.is_hitler = False
        ep = ExecutionPhase()

        res = ep.execute_player(player)
        assert not player.alive
        assert res is None

        player.alive = True
        player.is_hitler = True

        res = ep.execute_player(player)
        assert not player.alive
        assert res == 'Game over -- Hitler has been shot!'

    def test_action(self):
        player = Mock()
        ep = ExecutionPhase()
        ep.execute_player = Mock()
        ep.action(player)
        ep.execute_player.assert_called_once_with(player)


class TestChooseNextPresidentPhase:

    def test_choose_next_president(self):
        player = Mock()
        player.is_president = False
        cnpp = ChooseNextPresidentPhase()
        cnpp.choose_next_president(player)
        assert player.is_president

    def test_action(self):
        player = Mock()
        cnpp = ChooseNextPresidentPhase()
        cnpp.choose_next_president = Mock()
        cnpp.choose_next_president(player)
        cnpp.choose_next_president.assert_called_once_with(player)


class TestPeekPlayerPhase:

    def test_peek_player(self):
        player = Mock()
        other_player = Mock()
        player.inform_role = Mock()
        ppp = PeekPlayerPhase()
        ppp.player = player
        ppp.peek_player(other_player)
        player.inform_role.assert_called_once_with(other_player)

    def test_action(self):
        peeking_player = Mock()
        peeking_player.inform_role = Mock()
        peeked_player = Mock()

        ppp = PeekPlayerPhase()
        ppp.player = peeking_player
        ppp.choose_next_player = Mock()
        ppp.action(peeked_player)
        ppp.choose_next_player.assert_called_once_with(peeked_player)


class TestPeekDeckPhase:

    def test_peek_deck(self):
        player = Mock()
        player.inform_deck = Mock()
        deck = DrawDeck()
        top_3 = deck.cards[-3:]
        pdp = PeekDeckPhase()
        pdp.player = player
        pdp.peek_deck(deck)
        assert player.inform_deck.assert_called_once_with(deck.top(3))
