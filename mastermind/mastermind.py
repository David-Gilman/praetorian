import requests, json, sys
from itertools import permutations 

email = 'davidapgilman@gmail.com'

r = requests.post('https://mastermind.praetorian.com/api-auth-token/', data={'email':email})
r.json()
# > {'Auth-Token': 'AUTH_TOKEN'}
headers = r.json()
headers['Content-Type'] = 'application/json'

# Interacting with the game
r = requests.get('https://mastermind.praetorian.com/level/1/', headers=headers)
inp = r.json()
gladiators = inp['numGladiators']
guesses = inp['numGuesses']
rounds = inp['numRounds']
weapons = inp['numWeapons']

possible = list(permutations(range(weapons),gladiators))
for i in possible:
	print(i)


while resp is empty:
	
	r = requests.post('https://mastermind.praetorian.com/level/1/', data=json.dumps({'guess':guess}), headers=headers)
	print(r.json()['response'])
#print(r.json())


def check(guess, ans):
	resp = [len(list(set(guess).intersection(ans))),0]
	for i in range(len(guess)):
		if guess[i] == ans[i]:
			resp[1]+=1 
	return resp
