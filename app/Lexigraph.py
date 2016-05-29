class Lexigraph:

	def combos(self, word):
		combs = {word}
		
		combs.add(word[0])
		
		combs = combs | self.transpose(word)
		combs = combs | self.delete(word)
		combs = combs | self.substitutions(word)	
			
		return combs
	
	def transpose(self, word):
		
		transposes = {word}
		
		for i in xrange(1, len(word)):
			messedWord = list(word)
			temp = word[i-1]
			messedWord[i-1] = word[i]
			messedWord[i] = temp
			
			transposes.add("".join(messedWord))
		
		return transposes
	
	def delete(self, word):
		deletions = {word}
		
		for i in xrange(len(word) - 1):
			deletions.add(word[:i] + word [i+1:])
		
		#specially added to ensure no array index problems	
		deletions.add(word[:-1])
		return deletions

	def substitutions(self, word):
		substitutions = {word}
		alphabet='abcdefghijklmnopqrstuvwxyz'
		for i in xrange(1, len(word)-1):
			for l in alphabet:
				substitutions.add(word[0:i] + l + word[i+1:])
		return substitutions