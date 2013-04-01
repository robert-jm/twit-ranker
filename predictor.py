import cPickle as pickle
import fnmatch
import sys
import os
from collections import defaultdict

def recursive_glob(rootdir='.', pattern='*'):
    return [os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(rootdir)
            for filename in filenames
            if fnmatch.fnmatch(filename, pattern)]



if __name__=='__main__':
	arg = sys.argv[1:]

	for folder in arg:
		scores = [x for x in recursive_glob(folder,'*.score')]
		for filename in scores:
			print filename
			l = pickle.load(open(filename,'rb'))
			for book in l.keys():
				print 'book: ', book
				# senti score
				senti_sum = sum(l[book]['pol'])
				
				print 'sentiwordnet sum ',senti_sum
				if len(l[book]['pol'])!=0:
					print 'avg sentiwordnet ', senti_sum/len(l[book]['pol'])
				else:
					print 'avg sentiwordnet ', 0
				# cue
				cues = l[book]['cue']
				p, n = 0, 0
				print 'cues: ',cues
				for c in cues:
					print c
					p +=c[0]
					n +=c[1]
				print 'positive cue ',p
				print 'negative cue ', n
				if len(cues)!=0:
					print 'p cue avg ', p/len(cues)
					print 'n cue avg ', n/len(cues)
				#if len(l[book]['cue'])!=0:
				#	print 'avg cue ', cue_sum/len(l[book]['cue'])
				#else:
				#	print 'avg cue ', 0
				# emotion
				e_dict = defaultdict(int)
				for d in l[book]['emo']:
					for k, v in d.iteritems():
						e_dict[k] += v
				print e_dict
				# pmi
				pmi_sum = sum(l[book]['pmi'])
				print 'pmi sum ',pmi_sum
				if len(l[book]['pmi'])!=0:
					print 'avg pmi ', pmi_sum/len(l[book]['pmi'])
				else:
					print 'avg pmi ', 0
				print '==========='


