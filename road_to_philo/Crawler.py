import logging
import sys
import pickle
import networkx as nx

from .Webpage import WebPage

logger = logging.getLogger(__name__)


class Crawler:
    local_webpages_list = []
    global_webpages_list = []
    loops = {}
    graph = nx.DiGraph()

    def __init__(self, starting_url, mode='s'):
        self.steps = 0
        self.mode = mode
        self.starting_url = starting_url
        self.next_url = starting_url

    def add_step(self):
        self.global_webpages_list.append(self.title)
        self.local_webpages_list.append(self.title)
        self.graph.add_node(self.title)
        if self.steps > 0:
            self.graph.add_edge(self.local_webpages_list[self.steps - 1], self.title)
        self.steps += 1

    def _check_acyclic(self):
        title = self.title
        if title not in self.local_webpages_list:
            return True
        else:
            logger.info('Entered a loop! Back at: {}'.format(title))
            self.exit()

    def crawl(self):
        webpage = WebPage(self.next_url)
        self.title = webpage.title
        self._check_acyclic()
        if webpage.check_website_info() == 0:
            self.exit()
        logger.info('Step number: {} - {}'.format(self.steps, webpage.title))
        self.next_url = webpage.scrape_weblinks()
        if self.next_url is None:
            logger.info("No URLs to go to! Please try again")
            self.exit()
        self.add_step()
        self.crawl()

    def start(self):
        self.crawl()

    def exit(self):
        if self.title == 'Philosophy':
            self.add_step()

        if self.mode == 'i':
            self.next_url = 'https://en.wikipedia.org/wiki/special:random'
            logger.info("Starting from a new random topic!")
            self.steps = 0
            self.local_webpages_list = []
            self.crawl()
        else:
            logger.info("Terminating and saving data to crawlerData")
            with open('crawlerData', 'wb') as f:
                pickle.dump(self, f)
                f.close()
            sys.exit(0)
