import cPickle as pickle
import random

def wk_key(x):
	return int(x.split('k')[1])

def determine_label(curr, nxt):
	if curr>nxt:
		return -1
	if nxt> curr:
		return 1
	return 0

tops = pickle.load(open('tops.pkl','rb'))
dataset = []

def data_to_str(item):
	s =str(item[0])+" "
	for i in range(1,8):
		s += str(i)+":"+str(item[i])+" "
	return s+'\n'

# label: -1, 0, 1
# feature 1: neutral cues
# feature 2: sadness cues
# feature 3: joy cues
# feature 4: sentiword net score
# feature 5: neg cues
# feature 6: pos cues
# feature 7: pmi

for book, value in tops.iteritems():
	if len(value.keys()) <=1:
		continue
	sorted_weeks = sorted(value, key=wk_key)
	last_idx = len(sorted_weeks)
	for idx, wk in enumerate(sorted_weeks):
		if idx+1==last_idx:
			break
		data = {}
		if 'rank' not in value[wk]:
			continue
		curr = int(value[wk]['rank'])
		nxt = int(value[sorted_weeks[idx+1]]['rank'])
		data[0] = determine_label(curr, nxt)
		if 'emo' not in value[wk]:
			continue
		data[1] = value[wk]['emo']['neutral']
		data[2] = value[wk]['emo']['sadness']
		data[3] = value[wk]['emo']['joy']
		if 'avg_sent' not in value[wk]:
			continue
		data[4] = value[wk]['avg_sent']
		data[5] = value[wk]['n_cue']
		data[6] = value[wk]['p_cue']
		data[7] = value[wk]['pmi']
		dataset.append(data)

indices = random.sample(range(len(dataset)), int(len(dataset)*0.5))
train = [dataset[i] for i in sorted(indices)]
test = [x for x in dataset if x not in train]

print train
print len(train)

print '------'
print test
print len(test)

with open('strap.train', 'w') as f:
	for item in train:
		f.write(data_to_str(item))

with open('strap.test', 'w') as f:
	for item in test:
		f.write(data_to_str(item))


