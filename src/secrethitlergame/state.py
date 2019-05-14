import numpy as np
from secrethitlergame.players import SecretHitlerPlayer


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
            self.begin_enactment_process()
        else:
            self.push_to_next_president()

    def begin_enactment_process(self):
        last_card = self.played_cards[-1]
        self.discovered_card(last_card)
    
    def push_to_next_president(self):
        self.pres_seat += 1
        if self.standstill_count < 3:
            self.standstill_count += 1  
        else:
            self.topdeck()

    def topdeck(self):
        p_lib = self.n_liberals_left/self.cards_in_deck
        p_fasc = 1 - p_lib
        top_decked_card = np.random.choice(['L', 'F'], p=[p_lib, p_fasc])

        if top_decked_card == 'L':
            self.n_liberals_left -= 1
        else:
            self.n_fasc_left -= 1
        self.cards_in_deck -= 1
        self.standstill_count = 0 