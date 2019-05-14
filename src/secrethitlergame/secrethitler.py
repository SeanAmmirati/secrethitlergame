
from math import factorial
import numpy as np
from secrethitlergame.state import SecretHitlerState

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



sh = SecretHilter()
sh.vote_for_government('2', {'0': 'Ja', '1': 'Nein', '2': 'Ja', '3': 'Ja', '4': 'Ja', '5': 'Ja', '6':'Nein'})
sh.enact_policy([['L', 'F', 'F'], ['L', 'F']], ['F', 'F'], 'F')
sh.vote_for_government('4', {'0':'Ja', '1':'Nein', '2':'Ja', '3': 'Ja', '4': 'Ja', '5': 'Ja', '6':'Nein'})
sh.enact_policy([['L', 'F', 'F'], ['L', 'F']], ['L', 'F'], 'F')
sh.determine_suspicions()
