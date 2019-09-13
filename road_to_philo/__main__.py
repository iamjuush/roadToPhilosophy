import logging

from .Crawler import Crawler

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    topic = input('Please enter a starting topic name: \n')
    topic = topic.replace(" ", "_")
    topic_url = "https://en.wikipedia.org/wiki/%s" % topic
    logger.info("Initial URL: {}".format(topic_url))
    crawler = Crawler(topic_url)
    crawler.start()
