import pytest
import secrethitlergame

__author__ = "Sean Ammirati"
__copyright__ = "Sean Ammirati"
__license__ = "mit"


@pytest.fixture
def claim_lib():
    from secrethitlergame.claim import Claim
    return Claim(1, ['F', 'F'], 'chanc', 3, False, None)


@pytest.fixture
def clean_state_lib(scope='module'):
    from secrethitlergame.state import SecretHitlerState as State
    clean_state = State()
    return clean_state


def test_probability(claim_lib, clean_state_lib):
    assert claim_lib.probability(clean_state_lib) == (9/15) * (8/14)
