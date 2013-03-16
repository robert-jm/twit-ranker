from collections import namedtuple
import pickle
import lxml
from BeautifulSoup import BeautifulSoup
import unicodedata

WordFreq = namedtuple('WordFreq', ['rank','pos', 'frequency', 'dispersion'])

def incr(n):
	if n==4:
		return 0
	return n+1

m = {}
FILE="words.html"
cnt =0
rank, pos, freq, dis, key = '','','','',''
with open(FILE, 'rU') as f:
	soup = BeautifulSoup(f.read())
	for td in soup.findAll('td'):
		for tr in td:
			if cnt==0:
				rank = tr.rstrip()
			elif cnt==1:
				idx = tr.rfind(';')
				key = tr[idx+1:].rstrip()
			elif cnt==2:
				pos = tr.rstrip()
			elif cnt==3:
				freq = tr.rstrip()
			elif cnt==4:
				dis = tr.rstrip()
				m[key] = WordFreq(rank,pos, freq,dis)
			cnt = incr(cnt)

output = open('wordfreq.pkl', 'wb')
pickle.dump(m, output)
output.close()

