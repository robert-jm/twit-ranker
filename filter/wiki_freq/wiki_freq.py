import wikipedia
import wiki2plain

class WikiFreq:
	d = {}
	total = 0
	alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
	def __init__(self, title):
		lang = 'simple'
		wiki = wikipedia.Wikipedia(lang)
		r = ''
		try:
			r = wiki.article(title)
		except:
			print "Could not find article"
		if r:
			w = wiki2plain.Wiki2Plain(r)
			content = w.text
			self.calc_freq(content)

	def calc_freq(self, text):
		lst = text.split()
		for i in lst:
			boo = False
			for j in i:
				if j not in self.alphabet:
					boo = True
					break

			if not boo:
				if i in self.d.keys():
					temp = self.d[i]
					self.d[i] = temp+1
				else:
					self.d[i] = 1
				self.total += 1
		print self.total

