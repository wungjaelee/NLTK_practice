from bs4 import BeautifulSoup
from urllib import request
import re
import sys

STARTING_PHRASES = ['Dear Hiring Manager',
                    'To Whom It May Concern',
                    'Dear Director of Athletics',
                    'Dear Chief Pilot and Hiring Manager',
                    'Dear Director of Housing',
                    'Dear School Board']
ENDING_PHRASES = ['Sincerely']

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
    start = raw_text.find(starting_phrase)
    if start == -1:
        return ""
    end = raw_text.rfind(ending_phrase)
    if end == -1:
        return ""
    return raw_text[start:end]

def get_job_title(cv_url):
    return cv_url.split('/')[-1]

def find_cover_letter_content(raw_text):
    for starting_phrase in STARTING_PHRASES:
        for ending_phrase in ENDING_PHRASES:
            cv_content = parse_raw_text(raw_text, starting_phrase, ending_phrase)
            if cv_content:
                return cv_content
    print("cover letter content was not detected: " + cv_url)
    print("Consider modifying this code by adding appropriate starting_phrase or ending_phrase")
    return ""

def main():
    url = sys.argv[1]
    for cv_url in get_all_cover_letter_urls(url):
        print("processing: ", cv_url)
        html = request.urlopen(cv_url).read().decode('utf8')
        raw = BeautifulSoup(html, 'html.parser').get_text()

        cv_content = find_cover_letter_content(raw)

        job_title = get_job_title(cv_url)

        with open('./cover_letters/' + job_title + '.txt', 'w') as f:
            f.write(cv_content)


if __name__ == "__main__":
    main()
