from urllib2 import urlopen
import re
import cPickle

OVERVIEW_URL="http://www.nytimes.com/best-sellers-books/overview.html"

COMBINED_PRINT_EBOOK_FICTION=re.compile("""<h3><a href="(.+?)">COMBINED PRINT &AMP; E-BOOK FICTION</a></h3>""")
BOOK_TITLES=re.compile("""(?:bookName|sellingTitle)\">(.+?)(?:, )?</span>""")

def parse_week_url(pattern):
    u=urlopen(OVERVIEW_URL)
    page=u.read()
    return pattern.search(page).group(1)

def parse_books(url):
    u=urlopen(url)
    page=u.read()
    return BOOK_TITLES.findall(page)

def normalize(booklist):
    return [x.lower()+"\n" for x in booklist]

if __name__=="__main__":
    combined=parse_week_url(COMBINED_PRINT_EBOOK_FICTION)
    books=parse_books(combined)
    with open("%s.bkl" % combined.split('/')[-3], 'w') as booklist: # date
        booklist.writelines(normalize(books))
