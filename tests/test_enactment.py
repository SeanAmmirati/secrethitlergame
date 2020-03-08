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


def test_is_conflict(possible_actions_list):
    for action in possible_actions_list:
        e = Enactment(action['president_policy'],
                      action['chancelor_policy'])
        conflict = action['p_passed'] != action['c_draw']

        assert e.is_conflict() == conflict


@pytest.fixture
def possible_actions_list():
    """ setup any state specific to the execution of the given module."""

    card_types = [LiberalCard, FascistCard]
    three_card_combos = combinations_with_replacement(card_types, 3)
    two_card_combos = combinations_with_replacement(card_types, 2)

    possible_draw_claims_pres = [[Card()
                                  for Card in y]
                                 for y in three_card_combos
                                 ]

    possible_draw_claims_chanc = [[Card()
                                   for Card in y]
                                  for y in two_card_combos
                                  ]

    possible_actions_list = []
    for p_draw in possible_draw_claims_pres:
        for c_draw in possible_draw_claims_chanc:
            for j in range(len(p_draw)):
                p_passed = p_draw.copy()
                p_discard = p_passed.pop(j)
                for i in range(len(c_draw)):
                    c_played = c_draw.copy()
                    c_discard = c_played.pop(i)
                    c_played = c_played[0]
                    possible_actions_list.append(dict(
                        president_policy=PolicyAction(
                            RecievedClaim(p_draw),
                            DiscardClaim([p_discard])
                        ),
                        chancelor_policy=PolicyAction(
                            RecievedClaim(c_draw),
                            DiscardClaim([c_discard])
                        ),
                        enacted=c_played,
                        p_passed=p_passed,
                        c_draw=c_draw
                    ))

    return possible_actions_list
