from bs4 import BeautifulSoup
from urllib import request
import re
import sys

def get_all_cover_letter_urls(url):
    resp = request.urlopen(url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))
    cover_letter_urls = []
    for link in soup.find_all('a', href=True):
        link_info = link['href'].split('/')
        if len(link_info) == 4 and link_info[1] == 'career-advice':
            cover_letter_urls.append(url + '/' + link_info[-1])
    return cover_letter_urls

if __name__ == "__main__":
    main()
