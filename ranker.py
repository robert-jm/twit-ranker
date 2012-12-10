#!/usr/bin/env python

"""

The sentiment analysis module that computes polarity and intensity for each
tweet. Then, book ranks are computed based on the total sum of the tweet
scores. 

"""
__author__ = "Kent Chen"
__copyright__ = "Copyright 2012, Kent Chen"
__credits__ = []
__license__ = ""
__version__ = "0.1"
__maintainer__ = "Kent Chen"
__email__ = "kche@seas.upenn.edu"

import sentiwordnet
import tweet
from nltk.tag.stanford import POSTagger

# Hard coded path. Get all this into a config file in the future
tagger_path = '/Users/kent/twit-ranker/wsj-0-18-bidirectional-distsim.tagger'
tagger_jar_path = '/Users/kent/twit-ranker/stanford-postagger-3.1.4.jar'

# Lookup table. 'q' indicates that the pos should not get a score

pos_table = {'JJ': 'a'\
		'JJR': 'a'\
		'JJS': 'a'\
		'NN': 'n'\
		'NNP': 'n'\
		'NNPS': 'n'\
		'NNS': 'n'\
		'RB': 'r'\
		'RBR': 'r'\
		'RBS': 'r'\
		'VB':'v'\
		'VBD':'v'\
		'VBG':'v'\
		'VBN':'v'\
		'VBP':'v'\
		'VBZ':'v'
		}


class Ranker:
	def __init__(self, filename):
		"""
		Argument:
		filename -- path to the SentiWordNet file
		"""
		self.swn = SentiWordNetCorpusReader(filename);
		self.st = POSTagger(tagger_path, tagger_jar_path)
	
	def compute_score(tweets):
		"""
		Argument:
		tweets -- compute the tweet score for the input batch of tweets
		"""
		running_sum = 0
		for tweet in tweets:
			score, text = _evaluate_emoticons(tweet.text)
			pos = self.st.tag(text.split())
			for p in pos:
				val = _lookup_pos(p[1])
				if val == 'q':
					continue
				
				temp = self.swn.senti_synsets(p[0], val)
				for word in temp:
					score[0] = word.pos_score
					score[1] = word.neg_score
			if score[0] > score[1]:
				running_sum += score[0]:
			else:
				running_sum += -1*score[1]

		return running_sum


	def _evaluate_emoticons(self, text):
		"""
		Get rid of emoticons in tweet and convert emoticons to score. A score
		is a list object [posScore, negScore]
		"""
		score = [0,0]

		return score, text

	def _lookup_pos(pos):
		"""
		Convert POS to one of {'a', 's', 'n', 'r', 'v'} so sentiwordnet can
		score it. Note: n - NOUN, v - VERB, a - ADJECTIVE, s - ADJECTIVE
		SATELLITE, r - ADVERB 

		Note that Stanford POSTagger uses the Penn TreeBank tag set. Refer to
		this for a comprehensive list: http://www.computing.dcu.ie/~acahill/tagset.html
		"""
		if not (pos in pos_table):
			return 'q'

		return pos_table[pos]

	def rank(self, pairs):
		"""
		Argument:
		pairs -- A list of (book, tweets) tuples. book should be a book title(string) and tweets should be a list of tweets (class tweet)

		Return:
		ranking
		"""		
		scoreboard = {}
		for item in pairs:
			scoreboard[item[0]] = compute_score(item[1])
		from operator import itemgetter
		ranking = sorted(scoreboard.items(), key=itemgetter(1), reverse=True)
		# return [t[0] for t in ranking]
		return ranking

