import math
import operator
import sys
from collections import defaultdict
import os

all_books = {}

def comp_dictionary(arg):
	pmi = get_book_pmi(arg)
	d = {}
	for i in range(1, 16):
		e = {}
		score = 15
		for line in open('./' + str(i) + '.bkl'):
			s = line.split('|')
			book = s[0]
			e[book] = score
			all_books[book] = 0.0
			score -= 1
			if score == 0:
				break
		d[i] = e
	return calc_error(d, pmi)

def recursive_glob(rootdir='.', pattern='*'):
    return [os.path.join(rootdir, filename)
            for rootdir, dirnames, filenames in os.walk(rootdir)
            for filename in filenames
            if fnmatch.fnmatch(filename, pattern)]

def get_book_pmi(folders):
	book_pmi = defaultdict(int)
	for folder in folders:
		scores = [x for x in recursive_glob(folder,'*.score')]
		for filename in scores:
			l = pickle.load(open(filename,'rb'))
			for book in l.keys():
				book_pmi[book] += sum(l[book]['pmi'])
	return book_pmi


def calc_error(d,pmi):
	for book in all_books.keys():
		for i in range(1, 16):
			temp = d[i]
			score = 0.0
			try:
				score = temp[book]
			except:
				score = 0
			all_books[book] = all_books[book] + score * math.exp(i-16)
		print book.lower().replace(' ', '_')
		print pmi[book.lower().replace(' ', '_')]
		all_books[book] += pmi[book]*4
	sorted_x = sorted(all_books.iteritems(), key=operator.itemgetter(1))
	return sorted_x


if __name__=='__main__':
	arg = sys.argv[1:]
	print arg
	x = comp_dictionary(arg)
	x.reverse()
	print x
