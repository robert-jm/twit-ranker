import os
import re

# Parse stop list to hash set
stop_list = set()
for line in (open("../STOP_LIST",'r')).readlines():
    stop_list.add(line.strip())

reviews = os.listdir("./BOOKS/")
term_freq = {}
for f in reviews:
    inp = open("BOOKS/"+f,'r')
    for line in inp:
        line = line.strip()
        line = re.sub(r'\W+ ', '', line)
        for term in line.split():
            if term in stop_list or term[0].isupper():
                continue
            if term not in term_freq:
                term_freq[term] = 1
            else:
                term_freq[term] += 1

for key, value in sorted(term_freq.iteritems(), key=lambda (k,v): (v,k)):
    print key, value
