import urllib.parse as urlparse
import logging
from os import getenv

from .Crawler import Crawler

logger = logging.getLogger(__name__)


def handle(req):
    """handle a request to the function
    Args:
        req (str): request body
    """
    if len(req) != 0:
        input_topic = req
    else:
        input_topic = urlparse.parse_qs(getenv("Http_Query"))

    topic = input_topic.replace(" ", "_")
    topic_url = "https://en.wikipedia.org/wiki/%s" % topic
    logger.info("Initial URL: ", topic_url)
    crawler = Crawler(topic_url)
    crawler.start()

