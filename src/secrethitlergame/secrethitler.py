
from math import factorial
import numpy as np


class SecretHitlerState():

    def __init__(self, possible_lib_cards=6, n_cards=15,
                 n_players=7, n_fasc=2, names=None):
        self.turn = 1

        self.possible_liberals = possible_lib_cards
        self.cards_in_deck = n_cards
        self.possible_fasc = self.cards_in_deck - self.possible_liberals
        self.played_cards = []
        self.chanc_claims = []
        self.pres_claims = []
        self.vote_results = []

        self.governments = []

        self.n_liberals_left = self.possible_liberals
        self.n_fasc_left = self.possible_fasc

        self.cards_drawn_on_gov = 3

        self.n_players = n_players

        self.n_alive_players = self.n_players

        self.standstill_count = 0

        self.pres_seat = 0

        if names is None:
            self.players = {str(x): SecretHitlerPlayer(str(x), x)
                            for x in range(self.n_players)}
        else:
            self.players = {name: SecretHitlerPlayer(name, seat)
                            for seat, name in names.items()}
            assert len(self.players) == n_players

    @property
    def chanc(self):
        last_vote = self.vote_results[-1]
        if last_vote['result'] == 'Passed':
            chanc = last_vote['chanc']
        else:
            chanc = None
        return chanc

    @property
    def pres(self):
        for player in self.players.values():
            if player.seat == self.pres_seat:
                return player

    def discovered_card(self, card):
        if card.upper() == 'L':
            self.discovered_liberal()
        else:
            self.discovered_fasc()

    def discovered_liberal(self):
        self.n_liberals_left -= 1

    def discovered_fasc(self):
        self.n_fasc_left -= 1

    def determine_vote(self, chanc):
        votes = [player_obj.vote_info[-1]['vote']
                 for player_obj in self.players.values()]
        pct_in_favor = np.mean([vote.upper() == 'JA' for vote in votes])

        result_dict = {
                           'turn': self.turn,
                           'in_favor': [player_obj for player_obj in self.players.values()
                                        if player_obj.vote_info[-1]['vote'].upper() == 'JA'],
                           'against': [player_obj for player_obj in self.players.values()
                                       if player_obj.vote_info[-1]['vote'].upper() != 'JA'],
                           'pres': self.pres,
                           'chanc': chanc
                           }

        if pct_in_favor > .5:
            result_dict.update({'result': 'Passed'})
        else:
            result_dict.update({'result': 'Failed'})

        self.vote_results.append(result_dict)

    def update_claims(self):
        self.pres_claims.append({self.pres: self.pres.move_info[-1]})
        self.chanc_claims.append({self.chanc: self.chanc.move_info[-1]})

    def move_pres(self):
        self.turn += 1
        self.pres_seat += 1

    def after_failed_government(self):
        self.standstill_count += 1
        self.move_pres()

    def after_successful_gov(self):
        self.begin_enactment_process()
        self.governments.append([{'turn':self.turn,
                                  'pres': self.pres,
                                  'chanc': self.chanc,
                                  'result' : self.played_cards[-1]}])
        self.update_claims()
        self.standstill_count = 0
        self.move_pres()
        self.cards_in_deck -= self.cards_drawn_on_gov

    def determine_course_of_action(self):
        last_vote = self.vote_results[-1]

        if last_vote['result'] == 'Passed':
            self.begin_enactment_process(last_vote['chanc'])
        else:
            self.push_to_next_president()

    def begin_enactment_process(self):
        last_card = self.played_cards[-1]
        self.discovered_card(last_card)


class Claim:
    def __init__(self, turn, claim, role,
                 co_governor, conflict, conflict_claim):
        self.turn = turn
        self.claim = claim
        self.role = role
        self.co_governor = co_governor
        self.conflict = conflict
        self.conflict_claim = conflict_claim

    def probability(self, state):
        if len(self.claim) == 0:
            return np.nan

        if isinstance(self.claim[0], list):
            claim = self.claim[0]
        else:
            claim = self.claim

        n_liberals = len([x for x in claim if x.upper() == 'L'])
        n_fascists = state.cards_drawn_on_gov - n_liberals

        n_ways_of_getting_liberals = factorial(state.n_liberals_left) / (factorial(state.n_liberals_left - n_liberals) * factorial(n_liberals)) if n_liberals < state.n_liberals_left else 0
        n_ways_of_getting_fasc = factorial(state.n_fasc_left) / (factorial(state.n_fasc_left - n_fascists) * factorial(n_fascists)) if n_fascists < state.n_fasc_left else 0
        n_pos_draws = factorial(state.cards_in_deck + 2) / (factorial(state.cards_in_deck - 1) * 6)

        import pdb; pdb.set_trace()
        prob = (n_ways_of_getting_liberals * n_ways_of_getting_fasc) / n_pos_draws
        return prob


class SecretHitlerPlayer():

    def __init__(self, name, seat):
        self.name = name
        self.appointments = []
        self.move_info = []
        self.vote_info = []
        self.status = 'Alive'
        self.seat = seat

    @property
    def conflicts(self):
        conflicts = [move for move in self.move_info if move.conflict]
        return conflicts

    @property
    def aggreeability(self):
        if len(self.move_info) == 0:
            return np.nan
        else:
            return np.mean([not move.conflict for move in self.move_info])

    @property
    def confidence(self):
        if len(self.vote_info) == 0:
            return np.nan
        else:
            return np.mean([vote['vote'].upper() == 'JA' for vote in self.vote_info])


    def appoint(self, turn, co_governor):
        info_dict = {
            'turn': turn,
            'appointed': co_governor
            }
        self.appointments.append(info_dict)

    def add_claim(self, turn, claim, role, co_governor, conflict, conflict_claim):
        claim = Claim(turn, claim, role, co_governor, conflict, conflict_claim)
        self.move_info.append(claim)

    def add_vote(self, turn, vote, vote_on_pres, vote_on_chanc):
        info_dict = {
            'turn': turn,
            'vote': vote,
            'vote_on_pres': vote_on_pres,
            'vote_on_chanc': vote_on_chanc
            }
        self.vote_info.append(info_dict)


class SecretHilter():

    def __init__(self, init_state=None):
        self.state = SecretHitlerState() if init_state is None else init_state

    def vote_for_government(self, chanc, votes):
        self.state.pres.appoint(self.state.turn, self.state.players[chanc])
        for voter, vote in votes.items():
            self.state.players[voter].add_vote(
                self.state.turn, vote,
                self.state.pres, self.state.players[chanc])

        self.state.determine_vote(self.state.players[chanc])

    def enact_policy(self, pres_claim, chanc_claim, played_card):
        pres = self.state.pres
        chanc = self.state.chanc

        conflict = chanc_claim != pres_claim[1]
        conf_claim_pres = None if not conflict else chanc_claim
        conf_claim_chanc = None if not conflict else pres_claim

        pres.add_claim(self.state.turn, pres_claim, 'president',
                       chanc, conflict, conf_claim_pres)
        chanc.add_claim(self.state.turn, chanc_claim, 'chancellor',
                        pres, conflict, conf_claim_chanc)

        self.state.played_cards.append(played_card)
        self.state.after_successful_gov()

    def determine_suspicions(self):
        print({name: player.move_info[-1].probability(self.state)
               for name, player in self.state.players.items()
               if len(player.move_info) > 0})


if __name__ == '__main__':
    sh = SecretHilter()
    sh.vote_for_government('2', {'0': 'Ja', '1': 'Nein', '2': 'Ja', '3': 'Ja', '4': 'Ja', '5': 'Ja', '6':'Nein'})
    sh.enact_policy([['L', 'F', 'F'], ['L', 'F']], ['F', 'F'], 'F')
    sh.vote_for_government('4', {'0':'Ja', '1':'Nein', '2':'Ja', '3': 'Ja', '4': 'Ja', '5': 'Ja', '6':'Nein'})
    sh.enact_policy([['L', 'F', 'F'], ['L', 'F']], ['L', 'F'], 'F')
    sh.determine_suspicions()
