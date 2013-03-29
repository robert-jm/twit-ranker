import sys
import requests
sys.path.append('../')
import word_freq_dictionary as w
import amazon_scraper 
from bs4 import BeautifulSoup
import google_search as g

class amaz_freq:
	total = 0.0
	alphabet = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
	eng_frequency = w.EnglishFrequency()
	threshold = 100

	def __init__(self, term):
		url = ''
		urls = g.search(term)
		for i in urls:
			if 'product-reviews' in i:
				url = i
		
		self.filt = []
		self.d = {}
		page = requests.get(url).text
		lst = amazon_scraper.get_page_reviews(page)
		self.calc_freq(lst[0])
		self.filt = self.generate_list()

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

	def generate_list(self):
		lst = self.d.keys()
		ret = []
		for i in lst:
			temp = 0
			try:
				temp = self.eng_frequency.get_freq(i.lower())
			except:
				temp = 0 #Word not in the english language
			if self.d[i] / self.total >= self.threshold * temp:
				ret = ret + [i]
		if 'PermalinkComment' in ret:
			ret.remove('PermalinkComment')
		if 'Amazon' in ret:
			ret.remove('Amazon')
		if 'reviews' in ret:
			ret.remove('reviews')
#		ret.remove('Wikia')
#		ret.remove('website')
#		ret.remove('websites')
		return ret	
