import sys
import os
import fnmatch
import cPickle as pickle
import analyzer as az
from collections import defaultdict

def recursive_glob(rootdir='.', pattern='*'):
    return [os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(rootdir)
            for filename in filenames
            if fnmatch.fnmatch(filename, pattern)]




if __name__ == '__main__':
	if len(sys.argv)==1:
		print 'usage: python computer.py folder1 folder2 ...'
		sys.exit(0)
	
	arg = sys.argv[1:]
	analyzer = az.Analyzer()
	
	# processed every book in folder
	for week in arg:
		analyzer.reset_cnt()
		notes = {}
		books = [x for x in recursive_glob(week, '*.pkl')]
		print books
		for b in books:
			l = pickle.load(open(b, 'rb'))
			bookname = os.path.basename(b).split('.')[0]
			print 'bookname: ',bookname
			notes[bookname] = defaultdict(list)
			for item in l:
				tokens, pos = item[0], item[1]
				pol_tmp = notes[bookname]['pol']
				pol_tmp.append(analyzer.get_polarity_score(tokens,pos))
				notes[bookname]['pol'] = pol_tmp
				#notes[bookname]['pol'].append(analyzer.get_polarity_score(tokens,pos))
				print tokens
				cue_tmp = notes[bookname]['cue']
				print 'computer before:',cue_tmp
				cue_tmp.append(analyzer.count_cue(tokens,pos))
				print 'computer after; ',cue_tmp
				notes[bookname]['cue'] = cue_tmp
				#notes[bookname]['cue'].append(analyzer.count_cue(tokens,pos))
				emo_tmp = notes[bookname]['emo']
				emo_tmp.append(analyzer.get_emotion(tokens))
				notes[bookname]['emo'] = emo_tmp
				#notes[bookname]['emo'].append(analyzer.get_emotion(tokens))
				analyzer.count(tokens,pos)
			for item in l:
				tokens, pos = item[0], item[1]
				pmi_tmp = notes[bookname]['pmi']
				pmi_tmp.append(analyzer.pmi(tokens))
				notes[bookname]['pmi'] = pmi_tmp
				#notes[bookname]['pmi'].append(analyzer.pmi(tokens))
		pickle.dump(notes, open(week+'.score','wb+'))
		print 'saved data in ', week+'.score'


