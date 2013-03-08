

class EnglishFrequency:
	freq_dict = {}
	def __init__(self):
		f = open("../all.num.o5", 'r')
		lst = []
		for line in f:
			lst = line.split()
			if lst[1] not in self.freq_dict:
				self.freq_dict[lst[1]] = int(lst[0]) / 100106029.0

	def get_freq(self, word):
		return self.freq_dict[word]

