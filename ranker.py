import sys
import os
import fnmatch
import operator
import glob
import cPickle as pickle
from collections import defaultdict

def recursive_glob(rootdir='.', pattern='*'):
    return [os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(rootdir)
            for filename in filenames
            if fnmatch.fnmatch(filename, pattern)]

def rank_by_aggregate_pmi(folders):
	book_pmi = defaultdict(int)
	for folder in folders:
		scores = [x for x in recursive_glob(folder,'*.score')]
		for filename in scores:
			l = pickle.load(open(filename,'rb'))
			for book in l.keys():
				book_pmi[book] += sum(l[book]['pmi'])
	sorted_x = sorted(book_pmi.iteritems(),
		key=operator.itemgetter(1))
	sorted_x.reverse()
	return [x[0] for x in sorted_x]


def get_stat(d):
	sortedkeys = sorted(d, key=lambda key: int(key.split('k')[1]))
	for k in sortedkeys:
		if 'avg_sent' not in d[k] or 'rank' not in d[k]:
			continue
		else:
			print '++++++++++++++++'
			print k
			print 'rank: ', d[k]['rank']
			print 'average sentiment: ',d[k]['avg_sent']
			print 'cue: ', d[k]['cue']
			print 'p_cue: ', d[k]['p_cue']
			print 'n_cue: ', d[k]['n_cue']
			print 'emo: ', d[k]['emo']
			print 'pmi: ', d[k]['pmi']
			print '++++++++++++++++'


def neutral_classifier(emo):
	total = sum(emo.values())
	if emo['neutral']/float(total) >=0.97:
		return 1
	else:
		return -1

def sadness_classifier(emo):
	if emo['sadness']>=2:
		return 1
	else:
		return -1

def joy_classifier(emo):
	total = sum(emo.values())
	if emo['joy']/float(total)>=0/01:
		return 1
	else:
		return -1

def senti_classifier(score):
	if score>=2:
		return -1
	else:
		return 1

def num_cue_classifier(cues):
	if cues>=50:
		return 1
	else:
		return -1

def neg_classifier(n_cues):
	if n_cues >= 30:
		return 1
	else:
		return -1

def pos_classifier(p_cues, n_cues):
	cues = p_cues + n_cues
	if p_cues/float(cues) > n_cues/float(cues):
		return 1
	else:
		return -1

def pmi_classifier(pmi):
	if pmi>=0.5:
		return -1
	else:
		return 1

def fusion_classifer(d):
	s=neutral_classifier(d['emo'])+sadness_classifier(d['emo'])+joy_classifier(d['emo'])
	s+=senti_classifier(d['avg_sent'])+num_cue_classifier(d['cue'])+neg_classifier(d['n_cue'])
	s+=pos_classifier(d['p_cue'], d['n_cue'])
	s+=pmi_classifier(d['pmi'])

	return s

# For every book, map week -> {rank, all kinds of stats}

if __name__ =='__main__':
	arg = sys.argv[1:]
	#print rank_by_aggregate_pmi(arg)

	ranks = defaultdict(lambda : defaultdict(dict))
	booklists = glob.glob('./nyt-lists/*.bkl')

	for bl in booklists:
		week = os.path.basename(bl).split('.')[0]
		with open(bl, 'rU') as f:
			for idx, line in enumerate(f):
				title = line.split('|')[0].lower().replace(' ','_')
				ranks[title][week]['rank'] = idx+1

	scores = glob.glob('./scores/*.score')

	#for folder in arg:
		#scores = [x for x in recursive_glob(folder,'*.score')]
	for filename in scores:
		basename = os.path.basename(filename)
		week = basename.split('.')[0]
		l = pickle.load(open(filename,'rb'))
		for book in l.keys():
			senti_sum = sum(l[book]['pol'])
			if len(l[book]['pol'])!=0:
				ranks[book][week]['avg_sent'] = senti_sum/len(l[book]['pol'])
			else:
				ranks[book][week]['avg_sent'] = 0
			
			p, n = 0, 0
			cues = l[book]['cue']
			for c in cues:
				p +=c[0]
				n +=c[1]
			ranks[book][week]['cue'] = p+n
			if len(cues) !=0:
				ranks[book][week]['p_cue'] = p/len(cues)
				ranks[book][week]['n_cue'] = n/len(cues)
			else:
				ranks[book][week]['p_cue'] = 0
				ranks[book][week]['n_cue'] = 0

			e_dict = defaultdict(int)
			for d in l[book]['emo']:
				for k, v in d.iteritems():
					e_dict[k] += v
			ranks[book][week]['emo'] = e_dict

			
			pmi_sum = sum(l[book]['pmi'])
			if len(l[book]['pmi'])!=0:
				ranks[book][week]['pmi'] = pmi_sum/len(l[book]['pmi'])
			else:
				ranks[book][week]['pmi'] = 0



# Sort the whole list of books be descending number of received tweets. 

cues_d = {}
for k,v in ranks.iteritems():
	count = 0
	for key, items in v.iteritems():
		if 'cue' in items:
			count += items['cue']
	cues_d[k] = count

tops = sorted(cues_d, key=cues_d.get, reverse=True)[:20]

t_d = {}
for t in tops:
	t_d[t] = dict(ranks[t])

pickle.dump(t_d, open('tops.pkl','wb'))


