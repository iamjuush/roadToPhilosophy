import logging
import threading
import pickle

from .Crawler import Crawler

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)


def main():
    mode = input('Please enter a mode \n i - Infinite mode) \n s - Single mode \n')
    while mode != 'i' and mode != 's':
        logger.info("Not a valid mode, please try again")
        mode = input('Please enter a mode \n i - Infinite mode) \n s - Single mode \n')
    topic = input('Please enter a starting topic name: \n')
    topic = topic.replace(" ", "_")
    topic_url = "https://en.wikipedia.org/wiki/%s" % topic
    logger.info("Initial URL: {}".format(topic_url))
    crawler = Crawler(topic_url, mode)
    crawler.start()


if __name__ == '__main__':
    try:
        thread = threading.Thread(target=main, daemon=True)
        thread.start()
        while thread.is_alive():
            thread.join(1)
    except KeyboardInterrupt:
        logger.info("Terminating program, data saved to crawlerData")
        with open('crawlerData', 'wb') as f:
            pickle.dump(Crawler.graph, f)
            f.close()