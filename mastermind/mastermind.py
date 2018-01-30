import requests, json, sys
from itertools import permutations 


def check(guess, ans):
    resp = [len(list(set(guess).intersection(ans))), 0]
    for i in range(len(guess)):
        if guess[i] == ans[i]:
            resp[1] += 1
    return resp


email = 'davidapgilman@gmail.com'

r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email':email})
r.json()
# > {'Auth-Token': 'AUTH_TOKEN'}
headers = r.json()
headers['Content-Type'] = 'application/json'
print(headers)

# Interacting with the game
r = requests.get('https://mastermind.praetorian.com/level/2/', headers=headers)
inp = r.json()
print(inp)
gladiators = inp['numGladiators']
guesses = inp['numGuesses']
rounds = inp['numRounds']
weapons = inp['numWeapons']

possible = list(permutations(range(weapons),gladiators))

i = 0
while i <= guesses:
    guess = possible[0]
    print(guess)
    r = requests.post('https://mastermind.praetorian.com/level/1/', data=json.dumps({'guess':guess}), headers=headers)
    print(r.json())
    print(r.json()['response'])
    combo = r.json()['response']
    possible.remove(guess)
    for p in possible:
        if check(p, guess) != combo:
            possible.remove(p)
    print(len(possible))
    print(str(i))
    i += 1