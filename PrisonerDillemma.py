import numpy as np

class PD:
    def __init__(self, player1, player2, lobbyName = "Default"): # TODO: make Player class
        self.p1 = player1
        self.p2 = player2

        newP1state = "InGame__" + self.p2.name
        newP2state = "InGame__" + self.p1.name
        if self.p1.waiting: # It just choose to be in the game
            self.p1.feedback(newP1state, 0, self.actions(newP1state))
        else:
            self.p1.current = newP1state # Just roughly plop it. We'll have event handlers soon, though.
        if self.p2.waiting: # It just choose to be in the game
            self.p2.feedback(newP2state, 0, self.actions(newP2state))
        else:
            self.p2.current = newP2state # Just roughly plop it. We'll have event handlers soon, though.

        # I wanted the advantage from defecting to be much smaller than the damage done by it.
        # Also, all rewards are positive; you always want to be picked.
        self.payoffs = {"vouch_vouch":(10, 10), "vouch_defect":(0, 12), "defect_vouch":(12, 0), "defect_defect":(5, 5)}
        self.lobby = lobbyName

    def combStrings(self, s1, s2):
        return s1 + "_" + s2

    def actions(self, state="InGame"):
        if state.startswith("InGame"):
            return ["vouch", "defect"]
        else:
            return ["returnToLobby"]

    def game(self):
        As = self.actions()
        move1 = self.p1.move(As) # This is the signature for "move", then. Takes action list, not full env.
        move2 = self.p2.move(As)
        newState1 = self.combStrings(move1, move2)
        newState2 = self.combStrings(move2, move1)
        reward1, reward2 = self.payoffs[newState1]
        self.p1.feedback(newState1, reward1, self.actions(newState1))
        self.p2.feedback(newState2, reward2, self.actions(newState2))
        return newState1

