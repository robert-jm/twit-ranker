import pycurl, json, HTMLParser

STREAM_URL="https://stream.twitter.com/1.1/statuses/sample.json"

USER="twitter-username"
PASS="twitter-password"

with open('2012-12-09.bkl', 'r') as booklist:
    stemmed={}
    for escbook in [x.strip() for x in booklist.readlines()]:
        book=HTMLParser.HTMLParser().unescape(escbook)
        nothe=book.replace('the ', '')
        noa=book.replace('a ', '')
        noan=book.replace('an ', '')
        nothea=nothe.replace('a ', '')
        nothean=nothe.replace('an ', '')
        noaan=noa.replace('an ', '')
        stemmed[nothe]=book
        stemmed[noa]=book
        stemmed[noan]=book
        stemmed[nothea]=book
        stemmed[nothean]=book
        stemmed[book]=book

    strs=stemmed.keys()
    print strs
    
class Client:
    def __init__(self):
        self.buffer=""
        self.conn=pycurl.Curl()
        self.conn.setopt(pycurl.USERPWD, "%s:%s" %(USER,PASS))
        self.conn.setopt(pycurl.URL, STREAM_URL)
        self.conn.setopt(pycurl.WRITEFUNCTION, self.on_receive)
        self.conn.perform()

    def on_receive(self, data):
        self.buffer+=data
        if data.endswith("\r\n") and self.buffer.strip():
            content=json.loads(self.buffer)
            self.buffer=""
            if not 'delete' in content and 'RT' in content['text']:
                if not 'retweeted_status' in content:
                    for book in strs:
                        if book in content['text'].lower():
                            print "%s\t%d\t%s" % (stemmed[book], content['id'], content['text'])
                    

if __name__=="__main__":
    client=Client()
