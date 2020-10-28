import numpy as np
from PrisonerDillemma import *

class Lobby:
    def __init__(self, label, playerList = []):
        self.label = label
        for player in playerList:
            player.current = 'inLobby' # Label goes here later.
        self.players = dict(zip([pl.name for pl in playerList], playerList))
        self.numPlayers = len(playerList)

    def removePlayer(self, playerName):
        return self.players.pop(playerName)

    def addPlayer(self, newPlayer):
        try:
            oldPlayer = self.players[newPlayer.name]
            raise(ValueError, "There is already a player named " + newPlayer.name)
        except KeyError:
            self.players[newPlayer.name] = newPlayer
        return None

    def actions(self, playerName):
        As = list(self.players.keys())
        As.remove(playerName)
        return As

    def turn(self, playerName):
        # First, the opponent selection
        player = self.players[playerName]
        playerActions = self.actions(playerName)
        opponent = self.players[player.move(playerActions)]
        opponentActions = self.actions(opponent.name)
        ##i CRUDE! FIX!! Event handlers belong here.
        opponent.waiting = True
        opponent.lastAction = player.name
        ##
        ## Then, the game itself.
        pd = PD(player, opponent)
        pd.game()
        ## THen, some bureaucracy around returning here.
        newActions = ['returnToLobby']
        newState = 'inLobby'
        newReward = 0
        player.move(newActions) # Only one choice
        player.feedback(newState, newReward, playerActions)
        opponent.move(newActions)
        opponent.feedback(newState, newReward, opponentActions)

    def round(self):
        for key in self.players.keys():\
            self.turn(key)






