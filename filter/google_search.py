import urllib
import json as m_json

# Gets top four Google Search results for the input term.
def search(term):
	query = urllib.urlencode ( { 'q' : term } )
	response = urllib.urlopen ( 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&' + query ).read()
	json = m_json.loads ( response )
	results = json [ 'responseData' ] [ 'results' ]
	urls = []
	for result in results:
		title = result['title']
		url = result['url']   # was URL in the original and that threw a name error exception
		print (url)
		urls.append(url)
	return urls
	
