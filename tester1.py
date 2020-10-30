from agent import *
from PrisonerDillemma import *
from lobby import *



rounds = 10000

a = Agent('ada')
g = Grouch('oscar')
s = Sucker('bobby')

l = Lobby('default', [a, g, s])


def main():
    for res in l.round():
        print(res)

for i in range(rounds):
    print("Round " + str(i))
    main()

