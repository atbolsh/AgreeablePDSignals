import numpy as np

class PD:
    def __init__(self, player1, player2, lobbyName = "Default"): # TODO: make Player class
        self.p1 = player1
        self.p2 = player2
        # TODO: after initial testing, make this into a state the player asks for and receives, not this rude assignment.
        self.p1.current = "InGame__" + self.p2.name
        self.p2.current = "InGame__" + self.p1.name
        self.payoffs = {"vouch_vouch":(10, 10), "vouch_defect":(0, 20), "defect_vouch":(20, 0), "defect_defect":(5, 5)}
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

