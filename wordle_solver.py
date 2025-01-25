import datetime
import random
import requests
import json

class WordleSolver():
	"""Solves wordle using a web solver"""
	def __init__(self, cheat=False):
		self.TRIES = []
		self.TURN = len(self.TRIES)
		self.SYMBOLS = '?????'
		self.WORD = None
		self.GUESSES = []
		self.WORDS = []
		if cheat:
			print("Cheating! Getting answer...")
			print(self.cheat())
			input("Press enter to exit!")
			exit()
	def cheat(self, m=None, d=None, y=None):
		"""Apparently, wordle is pre-created per month. Future answers for the month appear to be located at:
		https://www.nytimes.com/svc/wordle/v2/{yyyy}-{mm}-{dd}.json
		This is only useful for testing against the correct answer. Completely blows the whole point...lol
		"""
		if m is None or d is None or y is None:
			t = datetime.datetime.now()
			if m is None:
				m = t.month
			if d is None:
				d = t.day
			if y is None:
				y = t.year
		if len(str(m)) == 1:
			#if month is one digit, add a 0
			m = f"0{m}"
		elif len(str(d)) == 1:
			#same for day
			d = f"0{d}"
		url = f"https://www.nytimes.com/svc/wordle/v2/{y}-{m}-{d}.json"
		r = requests.get(url)
		try:
			d = r.json()
		except Exception as e:
			print(f"Couldn't get json:", e)
			print(r.text)
			return r.text
		print("data:", d)
		word = d['solution']
		return word
	def testWord(self, word='SMART', symbols='?????', tries = []):
		self.WORD = word
		t = {}
		t['word'] = word
		t['symbols'] = symbols
		tries.append(t)
		url = "https://europe-west1-perpetual-pleasure.cloudfunctions.net/wordle-solve?wordlength=5&plurals=false&visit=b1bthzeem6"
		headers = {}
		headers["Content-Type"] = "application/json"
		data = json.dumps(tries)
		r = requests.post(url, data=data, headers=headers)
		try:
			out = tries, r.json()
		except:
			out = tries, r.text
		return out


	def guess(self, word, symbols='?????', tries=None):
		if word not in self.GUESSES:
			self.GUESSES.append(word)
		else:
			txt = f"Oops, already guessed that! ({word})"
			raise Exception(txt)
		if tries is None:
			tries = self.TRIES
		if tries != []:
			self.TURN = len(tries)-1
		else:
			self.TURN = 0
		if self.TURN == 0:
			tries, ret = self.testWord(word=word, symbols=symbols)
		else:
			tries, ret = self.testWord(word=word, symbols=symbols, tries=tries)
		self.TRIES = tries
		self.WORDS = ret["suggested_words"]
		return self.TRIES, ret

	def pickRdm(self, words):
		idx = random.randint(0, len(words)-1)
		return words[idx]

	def loop(self, answer=None):
		word = "SMART"
		tries = []
		symbols = "?????"
		run = True
		words = []
		while run:
			symbols = input("Enter symbols:")
			tries, ret = self.guess(word=word, symbols=symbols, tries=tries)
			print(ret)
			if ret["suggested_words"] == [] or symbols == '+++++':
				print("Won!")
				ct = len(tries)
				print(f"{ct} tries - {word}")
				run = False
				break
			else:
				word = self.pickRdm(ret["suggested_words"])
				if answer == word:
					print(f"Guessed it in {ct} tries! - {word}")
					run = False
					break
				print("Next guess:", word)
		return tries, word

if __name__ == "__main__":
	w = WordleSolver()
	answer = w.cheat()
	print(w.loop(answer=answer))
