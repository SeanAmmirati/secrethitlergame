class Enactment:

    def __init__(self,
                 president_action,
                 chancelor_action):

        self.president_action = president_action

        if chancelor_action.enacted_cards() is None:
            raise ValueError(
                'Chancellor must have made at least one valid action. Use [None, PlayedCard] if the chancelor makes no claim to the identity of the discarded card.')

        self.chancelor_action = chancelor_action

    def enacted_policy(self):
        return self.chancelor_action.enacted_cards()

    def is_conflict(self):
        return self.president_action.passed_cards() != self.chancelor_action.recieved_cards()


if __name__ == '__main__':
    from claim import RecievedClaim, DiscardClaim, PolicyAction
    p_rc = RecievedClaim([None, 'F', 'L'])
    p_dc = DiscardClaim([None])

    c_rc = RecievedClaim(['F', 'F'])
    c_dc = DiscardClaim(['F'])

    p_pol = PolicyAction(p_rc, p_dc)
    c_pol = PolicyAction(c_rc, c_dc)

    enactment = Enactment(p_pol, c_pol)
    print(enactment.enacted_policy())
    print(enactment.is_conflict())
