from agent import *
from PrisonerDillemma import *
from lobby import *
import json

rounds = 10000

a = Agent('ada')
g = Grouch('oscar')
s = Sucker('bobby')

l = Lobby('default', [a, g, s])

print("Three players in the lobby, ada, oscar and bobby.")
print("Agent:\tada")
print("Grouch:\toscar")
print("Sucker:\tbobby")
print("These are all simple Q-learning agents for now")
print("Here are the lobby rounds.")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\n\n")

def main():
    for res in l.round():
        print(res)

for i in range(rounds):
    print("Round " + str(i))
    main()

print("\n\n")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("\n\n")

print('\nHere is ada:')
print(json.dumps(a.__dict__))
print('\nHere is the grouch:')
print(json.dumps(g.__dict__))
print('\nHere is the sucker:')
print(json.dumps(s.__dict__))

