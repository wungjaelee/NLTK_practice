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

def parse_raw_text(raw_text, starting_phrase, ending_phrase):
    return raw_text[raw_text.find(starting_phrase):raw_text.rfind(ending_phrase)]

def get_job_title(cv_url):
    return cv_url.split('/')[-1]

def main():
    url = sys.argv[1]
    for cv_url in get_all_cover_letter_urls(url):
        print("processing: ", cv_url)
        html = request.urlopen(cv_url).read().decode('utf8')
        raw = BeautifulSoup(html, 'html.parser').get_text()

        cv_content = parse_raw_text(raw, 'Dear Hiring Manager,', 'Sincerely,')
        job_title = get_job_title(cv_url)

        with open(job_title + '.txt', 'w') as f:
            f.write(cv_content)


if __name__ == "__main__":
    main()
