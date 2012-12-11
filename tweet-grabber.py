import pycurl, json, HTMLParser, struct
from time import strptime
from calendar import timegm


STREAM_URL="https://stream.twitter.com/1.1/statuses/sample.json"

def get_twitter_info(filename):
    with open(filename, 'r') as info:
        u,_,p=info.read().strip().partition(',')
        return (u,p)

USER,PASS=get_twitter_info('twitter.password')

STRUCTFT="LI"

OUT_FILE='output'

TIMEFMT="%a %b %d %H:%M:%S +0000 %Y"

class Client:
    def __init__(self):
        self.output=open(OUT_FILE, 'wb+')
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
                    self.output.write(struct.pack(STRUCTFT, long(content['id_str']), timegm(strptime(content['created_at'], TIMEFMT))))
                    self.output.write(content['text'].encode('utf-8'))
                    self.output.write('\n')
                    self.output.flush()
                    #print "%s\t%d\t%s" % (stemmed[book], content['id'], content['text'])
                    

if __name__=="__main__":
    client=Client()
