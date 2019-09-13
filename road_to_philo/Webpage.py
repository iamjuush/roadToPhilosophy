import logging
import re
import sys

import requests
from bs4 import BeautifulSoup
from joblib import Memory

from . import CACHE_PATH

logger = logging.getLogger(__name__)
memory = Memory(CACHE_PATH, verbose=0)


@memory.cache
def get_webpage(url):
    logger.debug("Cache not used")
    r = requests.get(url)
    return r


def parenthetic_contents(string):
    """Generate parenthesized contents in string as pairs (level, contents)."""
    stack = []
    for i, c in enumerate(string):
        if c == '(':
            stack.append(i)
        elif c == ')' and stack:
            start = stack.pop()
            yield (len(stack), string[start + 1: i])


class WebPage:
    def __init__(self, url):
        if url == 'https://en.wikipedia.org/wiki/special:random':
            response = requests.get(url)
        else:
            response = get_webpage(url)
        self.url = url
        self.status_code = response.status_code
        self.html = response.text
        self.soup = None
        self.title = ""
        self._make_soup()
        self._p = ""
        self.next_url = ""

    def _make_soup(self):
        self.soup = BeautifulSoup(self.html, features='html.parser')
        self.title = self.soup.title.string.split('-')[0].strip()

    def check_website_info(self):
        if self._check_404():
            sys.exit(0)
        if self._check_philosophy():
            sys.exit(0)
        return

    def _check_404(self):
        if self.status_code == 404:
            logger.info('No such wiki page (404). Please try another topic.')
            return True
        else:
            return False

    def _check_philosophy(self):
        if self.url == 'https://en.wikipedia.org/wiki/Philosophy':
            logger.info('Reached Philosopy!')
            return True
        else:
            return False

    def filter_links(self, links):
        p_text = list(parenthetic_contents(self._p))
        for link in links:
            url = link.get('href')
            if sum([str(link) in level[1] for level in p_text]) > 0:  # This means that link is within parenthesis
                continue
            if url is None:
                continue
            if '#cite_note' in url:  # Skip citations
                continue
            if 'Help:IPA/' in url:  # Skip on how to pronounce
                continue
            if '.ogg' in url:  # SKip audio files for how to pronounce
                continue
            if 'File:' in url:  # Skip links that lead to files
                continue

            self.next_url = url
            return

        else:
            self.next_url = ""

    def check_url_type(self):
        if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', self.next_url):
            pass
        else:
            self.next_url = "https://en.wikipedia.org%s" % self.next_url

    def scrape_weblinks(self):
        paragraphs = self.soup.find_all('p')
        for p in paragraphs:
            self._p = str(p)
            links = p.find_all('a')
            if links:
                self.filter_links(links)
                if not self.next_url:
                    continue
                self.check_url_type()
                return self.next_url
        else:
            logger.info("No links for this article. Reached dead end. Please try again.")
            sys.exit(0)
