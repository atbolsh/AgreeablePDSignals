import numpy as np

class Agent:
    
    def __init__(self, name, initial = str("inLobby"), gamma = 1.0, alpha = 0.5, eps=0.3):
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





 
