import math
import operator

all_books = {}

def comp_dictionary():
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
	return calc_error(d)

def calc_error(d):
	for book in all_books.keys():
		for i in range(1, 16):
			temp = d[i]
			score = 0.0
			try:
				score = temp[book]
			except:
				score = 0
			all_books[book] = all_books[book] + score * math.exp(i-16)
	sorted_x = sorted(all_books.iteritems(), key=operator.itemgetter(1))
	return sorted_x



