import re

# Word files to use for filtering
REF_WORDS_FILE = "../book_reference_detection/master_list.txt"
NOVEL_TITLE_FILE = ""
AUTHOR_NAME_FILE = ""
NOVEL_WORDS_INDEX_FILE = ""

# Configuration
COUNT_THRESHHOLD = 2

class ReferenceDetector:
    ref_words

    def __init__(self):
        f = open(REF_WORDS_FILE,'r')
        self.ref_words = set()
        for word in f:
            word = word.strip()
            self.ref_words.add(word)

    def detectReference(tweet):
        bucket = re.sub(r'\W+ ','',tweet).split()
        count = 0
        for word in bucket:
            if word in ref_words:
                count += 1
        if count >= COUNT_THRESHHOLD:
            return True
        return False

            


