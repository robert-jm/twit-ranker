import subprocess
import sys
import copy
from nltk.stem.wordnet import WordNetLemmatizer
import dictionary_reader as dr
import cPickle as pickle
import spell_checker as s
import fnmatch
import os

POSTAGGER_PATH = './ark-tweet-nlp-0.3.2'
PREPROCESSED_PATH = './preprocessed'
lmtzr = WordNetLemmatizer()


def recursive_glob(rootdir='.', pattern='*'):
    return [os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(rootdir)
            for filename in filenames
            if fnmatch.fnmatch(filename, pattern)]

def clean_bin(filename):
	out = open(filename+'.clean','w+')
	print 'cleaning ', filename
	with open(filename,'r') as f:
		for line in f:
			l = line.rsplit(':')
			out.write(l[1].strip()[12:])
	out.close()
	print 'done cleaning ', filename

def pos_tag(filename):
	"""
	Return a list of pos-tagged tweets in the format of [tokens, pos]
	"""
	print 'pos tagging ',filename
	l = []
	output = subprocess.Popen([POSTAGGER_PATH+'/runTagger.sh', filename], stdout=subprocess.PIPE).communicate()[0]
	#output = subprocess.check_output(POSTAGGER_PATH+'/runTagger.sh '+filename,
	#		shell=True)

	for tweet in output.split('\n'):
		#print 'tweet: ', tweet
		elements = tweet.split('\t')
		#print elements
		if len(elements)<2:
			print 'WRONG'
			print elements
			print 'WRONG'
			continue
		tokens = elements[0].split()
		pos = elements[1].split()
		l.append([tokens,pos])
	print 'done pos tagging ', filename
	return l

def spell_check(l):
	"""
	Return a list of spell-checked, pos-tagged tweets in the format of [tokens, pos]
	"""
	print 'spellchecking '
	ret = []
	for tweet in l:
		tokens = []
		for t in tweet[0]:
			tokens.append(s.correct(t))
		ret.append([tokens, tweet[1]])
	print 'done spellchecking'
	return ret


def reduce_form(l):
	""" Stemming/lemmatizing + drop hashtag and handles
	"""
	print 'reducing'
	ret = copy.deepcopy(l)
	for tok, pos in ret:
		for idx, val in enumerate(tok):
			if (val[0]=='@' or val[0]=='#') and len(val)>1:
				val = val[1:]
				tok[idx] = val.lower()

			tag = pos[idx]
			if tag in dr.twitter2wordnet_tbl:
				tag = dr.twitter2wordnet_tbl[tag]
			else:
				continue
			
			tok[idx] = lmtzr.lemmatize(val, tag).lower()
	print 'done reducing'
	return ret

if __name__ == "__main__":
	if len(sys.argv)==1:
		print 'usage: python preprocessor.py folder1 folder2'
		sys.exit(0)
	
	arg = sys.argv[1:]
	# process every tweet file
	for fi in arg:
		files = [x for x in recursive_glob(fi) if '.' not in x]
		for filename in files:
			clean_bin(filename)
			l = pos_tag(filename+'.clean')
			l = spell_check(l)
			l = reduce_form(l)
			pickle.dump(l, open(filename+'.pkl', 'wb+'))

