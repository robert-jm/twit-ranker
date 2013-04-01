import os
import copy
from collections import namedtuple

MPQA_PATH = './dictionaries/mpqa-lexicon/subjclueslen1-HLTEMNLP05.tff'
BING_PATH_NEG = './dictionaries/opinion-lexicon-English/negative-words.txt'
BING_PATH_POS = './dictionaries/opinion-lexicon-English/positive-words.txt'
FRAMENET_PATH = './dictionaries/FrameNet-Emotion.txt'
WORDNETAFFECT_PATH ='./dictionaries/WordNetAffectEmotionLists/'
EMOTICONS_PATH = './dictionaries/emoticons.txt'

MPQA_Tuple = namedtuple('MPQA_Tuple', 'type len1 stemmed1 polarity')

# Twitter POS Tag conversion table

def get_mpqa():
  """
  Returns a mapping of (word, pos) -> attributes
  attributes include: type, len1, stemmed1, polarity

  """
  m = {}
  with open(MPQA_PATH, 'rU') as f:
    for line in f:
      item = line.rstrip().split(' ')
      tup = MPQA_Tuple(type=item[0].split('=')[1], len1=item[1].split('=')[1], stemmed1=(True if item[4].split('=')[1]=='y' else False), polarity=item[5].split('=')[1])
      word = item[2].split('=')[1]
      pos = item[3].split('=')[1]
      m[(word,pos)] = tup
  return m

def get_bing():
  """
  Returns a mapping of word -> {-1,1}
  """
  m = {}
  with open(BING_PATH_NEG, 'rU') as f:
	  for line in f:
		  m[line.rstrip()] = -1
  with open(BING_PATH_POS, 'rU') as f:
	  for line in f:
		  m[line.rstrip()] = 1
  return m

# problem with with(that).v
def get_framenet():
  """
  Returns a mapping of word -> list of pos
  """
  m = {}
  with open(FRAMENET_PATH, 'rU') as f:
    for line in f:
      print line
      words = line.rstrip().split(', ')  
      for item in words:
        if len(item)!=0: 
          pair = item.split('.')
          t = (pair[0].split('_')[0], pair[1])
          if t[0] in m:
            m[t[0]].append(t[1])
          else:
            m[t[0]] = list(t[1])
  return m

wordnet2mpqa_tbl = {'n': 'noun',
		'r':'adv',
		'v':'verb',
		'a':'adj'}

twitter2wordnet_tbl={
	'N': 'n',
	'V':'v',
	'A':'a',
	'R':'r',
		}

twitter2mpqa_tbl = {'N': 'noun',
		'V': 'verb',
		'A': 'adj',
		'R': 'adv'}

def get_affect():
	"""
	return a map that has word -> (polarity, emotion, POS)
		1 - positive, -1 - negative, 2 - both
	"""
	m = {}
	listing = os.listdir(WORDNETAFFECT_PATH)
	files = [x for x in listing if ".txt" in x]
	b_cat, n_cat = ["surprise"],["disgust", "anger", "fear", "sadness"]
	for fi in files:
		with open(WORDNETAFFECT_PATH+fi, 'rU') as f:
			cat = fi.split(".")[0]
			polarity = 1
			if cat in n_cat:
				polarity = -1
			elif cat in b_cat:
				polarity = 2
			for line in f:
				pos = line.rsplit()[0][0]
				if pos in wordnet2mpqa_tbl:
					pos = wordnet2mpqa_tbl[pos]
				else:
					continue
				items = [x for x in line.rsplit()[1:]]	
				
				for w in items:
					if "_" in w:
						w = w.split()[0]
					
					m[w] = (polarity, cat, pos)
	return m

def get_emoticons():
	"""
	Hand-compiled emoticons 
	map emoticon -> (polarity(-1 or 1), emotion) 
	emotion is one of {joy, disgust, anger, fear, sadness}
	"""
	m = {}
	with open(EMOTICONS_PATH, 'rU') as f:
		emo, polarity = 'joy', 1
		for line in f:
			if '#' in line:
				emo, polarity = line[1:].rsplit(',')
				continue
			emoticon = line.rsplit()[0]
			if emoticon in m:
				m[emoticon].append((int(polarity), emo))
			else:
				m[line.rsplit()[0]] = [(int(polarity), emo)]
	return m

class AffectDictionary:
	""" This dictionary uses WordNet Affect and the emoticon
	dictionary for the lookup function.

	"""
	def __init__(self):
		self.affect = get_affect()
		self.emoticons = get_emoticons()
	def lookup(self, token, pos=None):
		"""
		The function takes in a token and a pos (in twitter POS tag set
		standard)

		Polarity: -1(negative), 0(neutral), 1(positive), 2(both), 3(emotional)
		Emotion: joy, disgust, anger, fear, sadness, surprise, neutral
		return (polarity, emotion)
		"""

		if token in self.affect:
			return (self.affect[token][0], self.affect[token][1])

		if token in self.emoticons:
			return self.emoticons[token]

		return (0, 'neutral')


class BigDictionary:
	""" This dictionary uses WordNet Affect, Opinion Lexicon, MPQA and the emoticon
	dictionary for the lookup function.
	"""

	def __init__(self):
		self.bing, self.mpqa = get_bing(), get_mpqa()
		self.emoticons, self.affect = get_emoticons(), get_affect()

	def lookup(self,token, pos=None):
		"""
		The function takes in a token and a pos (in twitter POS tag set
		standard)

		Return -1(negative), 0(neutral), 1(positive), 2(both)
		"""
		if token in self.emoticons:
			return self.emoticons[token][0][0]

		if pos in twitter2mpqa_tbl:
			pos = twitter2mpqa_tbl[pos]

		if token in self.bing:
			return self.bing[token]
		if token in self.affect:
			return self.affect[token]
		if (token, pos) in self.mpqa:
			return self.mpqa[(token, pos)]
		return 0


