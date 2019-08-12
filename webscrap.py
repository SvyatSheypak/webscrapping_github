#!/usr/bin/env python3
"""This program is designed to scrap https://github.com/github
and write brief info on repos into a csv file:
name, link, description, language, tag1?tag2?tag3
"""

import argparse
from bs4 import BeautifulSoup
from contextlib import closing
from requests import get
from requests.exceptions import RequestException


def get_argparser():
    """Builds and returns a suitable argparser"""
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--file', nargs='?', type=str, default='out.csv',
                        help='an output file name')
    parser.add_argument('-u', '--url', nargs='?',
                        type=str, default='https://github.com/github',
                        help='an url to scrap, no guarantee\
                        on urls other than https://github.com/github')
    return parser


"""This three operations were looked up at
https://realpython.com/python-web-scraping-practical-introduction/
"""


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 and
            content_type is not None and
            content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def handle_empty_find(search_res):
    if not search_res:
        return ''
    else:
        return search_res.text.strip()


def prepare_str_to_csv(str_item):
    return '"' + str_item.replace('"', '""') + '"'


def extract_csv_from_li(li, source_url):
    name = handle_empty_find(li.find('a', itemprop='name codeRepository'))
    desc = handle_empty_find(li.find('p', itemprop='description'))
    url = li.find('a', itemprop='name codeRepository')
    if url != '':
        url = source_url + url['href'].split('/')[-1]
    tags = [x.text.strip() for x in
            li.find_all('a', class_="topic-tag topic-tag-link f6 my-1")]
    lang = handle_empty_find(li.find('span',
                                     itemprop="programmingLanguage"))
    items = [name, desc, url, lang, ', '.join(tags)]
    return ','.join([prepare_str_to_csv(x) for x in items])


def write_header(file):
    file.write(','.join(['name', 'description', 'url', 'lang', 'tags']) + '\n')


def parse_multipage_url_into_file(source_url, filename):
    with open(filename, 'w') as file:
        write_header(file)
        page = 1
        while True:
            # print("PAGE: ", page)
            cur_url = source_url + "?page={}".format(page)
            raw_html = simple_get(cur_url)
            soup = BeautifulSoup(raw_html, 'html.parser')
            find = soup.find_all('li', itemtype='http://schema.org/Code')
            if not find:
                break
            for li in find:
                file.write(extract_csv_from_li(li, source_url) + '\n')
            page += 1


def main():
    parser = get_argparser()
    args = parser.parse_args()
    outfile = args.file
    source_url = args.url
    parse_multipage_url_into_file(source_url, outfile)

if __name__ == "__main__":
    main()
