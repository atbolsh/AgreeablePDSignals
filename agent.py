import numpy as np

class Agent:
    
    def __init__(self, name, initial = str("inLobby"), gamma = 0.99, alpha = 0.5, eps=0.1):
        self.name = name
        self.initial = initial
        self.current = initial
        self.lastAction = "None"
        self.eps = eps
        self.alpha = alpha
        self.gamma = gamma
        self.waiting = False # Flag to wait after a move, for feedback.
        self.Q = {'EndEnd':0}
    
    def reset(self):
        self.current = self.initial
    
    def lookup(self, state, action):
        if state == 'End':
            return 0
        key = state + action
        try:
            q = self.Q[key]
        except KeyError:
            q = 0
            self.Q[key] = q
        return q
     
    def inclusiveArgMax(self, l):
        M = -1000000
        inds = []
        for i in range(len(l)):
            v = l[i]
            if v > M:
                M = v
                inds = [i]
            elif v == M:
                inds.append(i)
        return inds
    
    def greedyAction(self, actions):
        v = [self.lookup(self.current, action) for action in actions]
        inds = self.inclusiveArgMax(v)
        ind = np.random.choice(inds)
        return actions[ind]

    def exploringAction(self, actions):
        return np.random.choice(actions)
    
    def move(self, actions):
        if self.waiting:
            raise(ValueError, "Sorry, waiting for response.")

        if np.random.random() < self.eps:
            a = self.exploringAction(actions)
        else:
            a = self.greedyAction(actions)

        self.waiting = True
        self.lastAction = a
        return a

    def feedback(self, newState, R, newActions):
        if (not self.waiting):
            raise(ValueError, "Sorry, not waiting for response.")

        a = self.lastAction
        newMaxQ = max([self.lookup(newState, action) for action in newActions])
        
        key = self.current + a
        oldQ = self.lookup(self.current, a) # To insert it if not present
        self.Q[key] = oldQ + self.alpha*(R + (self.gamma*newMaxQ) - oldQ)
        
        self.current = newState
        self.waiting = False       
        return a, R

    def episode(self, env):
        self.reset()

        stateTrace = [self.current]
        actionTrace = []
        rewardTrace = []
        
        while self.current != "End":
            a, R = self.move(env)
            actionTrace.append(a)
            rewardTrace.append(R)
            stateTrace.append(self.current)
        
        return sum(rewardTrace), stateTrace, actionTrace, rewardTrace


class maimedAgent(Agent): # Method for limiting the abilities of Agents into a limited range
    def __init__(self, name, initial = str("inLobby"), gamma = 0.99, alpha = 0.5, eps=0.1):
        super(maimedAgent, self).__init__(name=name, initial=initial, gamma=gamma, alpha=alpha, eps=eps)

    def move(self, actions):
        if self.maimCondition(self.current):
            As = self.reduceActions(actions)
        else:
            As = actions
        return super(maimedAgent, self).move(As)

    def maimCondition(self, state): # To be overwritten as True in some cases
        return False

    def reduceAction(self, actions):
        return actions


class Grouch(maimedAgent):
    def __init__(self, name, initial = str("inLobby"), gamma = 0.99, alpha = 0.5, eps=0.1):
        super(Grouch, self).__init__(name=name, initial=initial, gamma=gamma, alpha=alpha, eps=eps)

    def maimCondition(self, state):
        return state.startswith("InGame")

    def reduceActions(self, actions):
        return [action for action in actions if action != 'vouch']

class Sucker(maimedAgent):
    def __init__(self, name, initial = str("inLobby"), gamma = 0.99, alpha = 0.5, eps=0.1):
        super(Sucker, self).__init__(name=name, initial=initial, gamma=gamma, alpha=alpha, eps=eps)

    def maimCondition(self, state):
        return state.startswith("InGame")

    def reduceActions(self, actions):
        return [action for action in actions if action != 'defect']

