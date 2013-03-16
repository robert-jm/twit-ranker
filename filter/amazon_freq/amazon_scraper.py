import requests
from bs4 import BeautifulSoup, NavigableString


def get_review_text(div):
    review_text = []
    for possible_text in div.children:
        if isinstance(possible_text, NavigableString):
            stripped_text = possible_text.strip()
            if len(stripped_text) > 0:
                review_text.append(stripped_text)
    return "\n".join(review_text)


def get_page_reviews(page_html):
    soup = BeautifulSoup(page_html)
    table = soup.find(id="customerReviews")
    y = soup.find_all("div", style = "margin-left:0.5em;")
    words = []
    for item in y:
	    item = item.text.split()
	    words.append(item)
    reviews = [" ".join(x) for x in words]
    return reviews
#    divs = table.tr.td.find_all("div", recursive=False)
 #   return [get_review_text(d) for d in divs]


def get_review_page_count(page_html):
    soup = BeautifulSoup(page_html)
    try:
        span = soup.find("span", class_="paging")
        links = span.find_all("a")
        target = links[-2]
        return int(target.text)
    except:
        return 1


def get_all_reviews(review_url):
    first_page = requests.get(review_url).text

    page_count = get_review_page_count(first_page)

    reviews = []
    urls = (review_url + "?pageNumber=" + str(i)
            for i in range(1, page_count + 1))
    for url in urls:
        review_html = requests.get(url).text
        reviews.extend(get_page_reviews(review_html))

    return reviews
