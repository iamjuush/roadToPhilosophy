import logging
import sys

from .Webpage import WebPage

logger = logging.getLogger(__name__)


class Crawler:
    visited_pages = []

    def __init__(self, starting_url):
        self.steps = 0
        self.starting_url = starting_url
        self.next_url = starting_url

    def add_step(self):
        self.steps += 1

    def _check_acyclic(self, title):
        if title not in self.visited_pages:
            self.visited_pages.append(title)
            return True
        else:
            logger.info('Entered a loop! Back at: {}'.format(title))
            sys.exit(0)

    def crawl(self):
        webpage = WebPage(self.next_url)
        self._check_acyclic(webpage.title)
        webpage.check_website_info()
        logger.info('Step number: {} - {}'.format(self.steps, webpage.title))
        self.next_url = webpage.scrape_weblinks()
        self.crawl()

    def start(self):
        self.crawl()
