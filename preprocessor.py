import subprocess
import sys
import cPickle as pickle

POSTAGGER_PATH = './ark-tweet-nlp-0.3.2'
PREPROCESSED_PATH = './preprocessed'

def pos_tag(filename):
	"""
	Return a list of pos-tagged tweets in the format of [tokens, pos]
	"""
	l = []
	output = subprocess.check_output(POSTAGGER_PATH+'/runTagger.sh '+filename)
	for tweet in output.split('\n'):
		elements = tweet.split('\t')
		tokens = elements[0].split()
		pos = elements[1].split()
		l.append([tokens,pos])

def spell_check(l):
	pass

def reduce_form(l):
	""" Stemming/lemmatizing + drop hashtag and handles
	"""
	pass

if __name__ = "__main__":
	arg = sys.argv[1:]
	# process every tweet file
	for filename in arg:
		l = pos_tag(filename)
		spell_check(l)
		reduce_form(l)
		pickle.dump(l, open('PREPROCESSED'+'/'+filename+'.pkl', 'wb'))
		

