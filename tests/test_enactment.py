from secrethitlergame.enactment import Enactment
from secrethitlergame.claim import RecievedClaim, DiscardClaim, PolicyAction
from secrethitlergame.cards import LiberalCard, FascistCard

from itertools import combinations, combinations_with_replacement
from collections import Counter

import pytest


def test_initialization(possible_actions_list):
    for action in possible_actions_list:
        e = Enactment(action['president_policy'],
                      action['chancelor_policy'])


def test_enacted_policy(possible_actions_list):
    for action in possible_actions_list:
        e = Enactment(action['president_policy'],
                      action['chancelor_policy'])
        assert e.enacted_policy() == [action['enacted']]


@pytest.fixture
def possible_actions_list():
    """ setup any state specific to the execution of the given module."""

    # No conflict, slightly nonsensible

    card_types = [LiberalCard, FascistCard]
    possible_draws = [[Card()
                       for Card in y]
                      for y in combinations_with_replacement(card_types, 3)
                      ]

    possible_actions_list = []
    for draw in possible_draws:
        for i in range(len(draw)):
            possible_discards = draw.copy()
            discard = possible_discards.pop(i)
            for j in range(len(possible_discards)):
                possible_chanc_discards = possible_discards.copy()
                c_discard = possible_chanc_discards.pop(j)
                possible_actions_list.append(dict(
                    president_policy=PolicyAction(
                        RecievedClaim(draw),
                        DiscardClaim([discard])
                    ),
                    chancelor_policy=PolicyAction(
                        RecievedClaim(possible_discards),
                        DiscardClaim([c_discard])
                    ),
                    enacted=possible_chanc_discards[0]))

    return possible_actions_list
