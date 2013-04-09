import glob
from collections import defaultdict

ranks = defaultdict(list)
booklists = glob.glob('./*.bkl')

for bl in booklists:
	with open(bl, 'rU') as f:
		for idx, line in enumerate(f):
			title = line.split('|')[0].lower()
			ranks[title].append(idx+1)
print ranks
