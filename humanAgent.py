import numpy as np

class HumanAgent:
    def __init__(self, name):
        self.name = name
        self.current = "inLobby"
        self.lastAction = "None"
        self.waiting = False

    def move(self, actions):
        if self.waiting:
            raise(ValueError, "Sorry, waiting for response.")

        print("\n\nHello " + self.name + "!")
        print("You are in state " + self.current)
        print("What would you like to do? Pick the corresponding number.")
        for i in range(len(actions)):
            print(str(i) + ")\t" + actions[i])

        while True:
            try:
                choice = int(input())
                if 0 <= choice < len(actions):
                    break
                else:
                    print("Sorry, that was not one of the options. Try again.")
            except ValueError:
                print("Sorry, response must be an integer.")

        a = actions[choice]
        self.lastAction = a
        self.waiting = True
        return actions[choice]

    def feedback(self, newState, R, newActions):
        if (not self.waiting):
            throw(ValueError, "Sorry, not waiting for response.")
        self.waiting = False
        print("\n\nHello " + self.name + "!")
        print("You were in state " + self.current)
        print("You played " + self.lastAction)
        print("You are now in state " + newState)
        print("During your turn, you will have options " + self.properify(newActions))
        self.current = newState
        print("You received a reward of " + str(R) + " sugar cubes.")
        print("Best of luck!\n\n")
        return self.lastAction, R

    def properify(self, stringList):
        n = len(stringList)
        if n == 0:
            return ''
        elif n == 1:
            return stringList[0]
        elif n == 2:
            return ' and '.join(stringList)
        else:
            return ', '.join(stringList[:-1] + " and " + stringList[-1])
 
