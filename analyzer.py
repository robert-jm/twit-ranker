import dictionary_reader as dr
import sentiwordnet as senti
import numpy
import operator
from collections import defaultdict

class Analyzer:
	pos_cnt = defaultdict(int)
	neg_cnt = defaultdict(int)

	def __init__(self):
		self.big = dr.BigDictionary()
		self.swn = senti.SentiWordNetCorpusReader('swn3.txt')
		self.affect = dr.AffectDictionary()

	def get_polarity_score(self, tweet, pos):
		"""
		input: 
		tweet is the preprocessed tweet text
		pos is the pos tag for each token
		output:
		an aggregate polarity score
		"""
		score = 0
		for idx, elem in enumerate(tweet):
			if pos[idx] not in dr.twitter2wordnet_tbl:
				continue
			tag = dr.twitter2wordnet_tbl[pos[idx]]
			synsets = self.swn.senti_synsets(elem, tag)
			if len(synsets)==0:
				continue
			t = synsets[0]
			if t.obj_score >=0.5:
				continue
			if t.pos_score> t.neg_score:
				score +=t.pos_score
			else:
				score += -1*t.neg_score
		return score

	def count_cue(self, tweet, pos, threshold=0):
		"""
		input: 
		tweet is the preprocessed tweet text
		pos is the pos tag for each token
		threshold is the minimum cues required to have a sentiment
		output:
		sentiment: +1 (positive), -1 (negative), 0 (neutral)
		"""
		posi, neg, tag = 0, 0, ''
		for idx, elem in enumerate(tweet):
			if pos[idx] not in dr.twitter2mpqa_tbl:
				tag = 'E' # assume it's emoticon
			else:
				tag = dr.twitter2mpqa_tbl[pos[idx]]
			sent = self.big.lookup(elem, tag)
			if sent<0:
				neg +=1
			elif sent==1:
				posi +=1
			elif sent >1:
				posi +=1
				neg +=1
		
		if posi==neg or (threshold>posi and threshold>neg):
			return 0
		return 1 if posi>neg else -1

	def get_emotion(self, tweet):
		"""
		input: 
		tweet is the preprocessed tweet text
		pos is the pos tag for each token
		output:
		joy, disgust, anger, fear, sadness, surprise, neutral
		"""
		emo = defaultdict(int)
		for elem in tweet:
			t = self.affect.lookup(elem)
			if len(t)==1:
				for e in t:
					emo[e[1]] +=1
			else:
				emo[t[1]] += 1
		#print emo
		#return max(emo, key=lambda x: emo.get(x))
		return emo

	def pmi(self, tweet):
		"""
		Compute the average SO of the tweet
		"""
		pmi = 0
		for token in tweet:
			pmi += numpy.log((0.01+Analyzer.pos_cnt[token])/(0.01+Analyzer.neg_cnt[token]))
			print pmi
		print pmi/len(tweet)
		
		return pmi/len(tweet)

	def count(self, tweet, pos):
		"""
		Count the cooccurence of each token in tweet and a sentiment cue. The
		result is stored in class variables. Make sure you run the function
		on all tweets before using the pmi function
		"""
		for idx, elem in enumerate(tweet):
			nbr = self._near(tweet, idx)
			Analyzer.pos_cnt[elem] += len([x for x in nbr if
				self.big.lookup(x,pos[idx])==1])
			Analyzer.neg_cnt[elem] += len ([x for x in nbr if
				self.big.lookup(x,pos[idx])==-1])
			both = len([x for x in nbr if self.big.lookup(x, pos[idx])==2])
			Analyzer.pos_cnt[elem]+= both
			Analyzer.neg_cnt[elem]+= both

	def reset_cnt(self):
		pos_cnt, neg_cnt = defaultdict(int), defaultdict(int)
	
	def _near(self,a, tok_idx, n=10):
		"""
		the NEAR operator: articles is a list of tokens
		"""
		before = a[:tok_idx][-n:]
		after = a[tok_idx:][1:n+1]
		return before+after


