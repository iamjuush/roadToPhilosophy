from bs4 import BeautifulSoup
import requests
import sys
import urllib.parse as urlparse
import re
import logging
from os import getenv

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

visited_pages = []


def select_link(links, para):
    for link in links:
        for item in para.contents:
            if link == item.next:
                break
        else:
            continue

        wiki_link = link.get('href')
        if wiki_link is None:
            continue

        elif '#cite_note' in wiki_link:
            continue

        elif 'Help:IPA/' in wiki_link:
            continue

        elif '.ogg' in wiki_link:
            continue

        elif 'File:' in wiki_link:
            continue

        else:
            first_link = wiki_link
            return first_link

    else:
        return None


def get_webpage(url):
    r = requests.get(url)
    if r.status_code == 404:
        return r, False
    else:
        return r, True


def check_acyclic(title):
    if title not in visited_pages:
        visited_pages.append(title)
        return True
    else:
        return False


def remove_word_origin(para, title):
    content = para.contents
    for idx, c in enumerate(content):
        if (title.strip().lower() in str(c).lower()) and ('(' in str(content[idx+1])):
            for i, item in enumerate(para):
                if ')' in item:
                    del para.contents[1:i+1]
                    return para
    else:
        return para





def main(url, steps):
    steps += 1
    r, http_ok = get_webpage(url)
    if not http_ok:
        logger.info('No such wiki page (404). Please try another topic.')
        sys.exit(0)

    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.string.split('-')[0]

    if not check_acyclic(title):
        logger.info('Entered a loop! Back at: {}'.format(title))
        sys.exit(0)

    logger.info('Step number: {} - {}'.format(steps, title))
    if url == 'https://en.wikipedia.org/wiki/Philosophy':
        logger.info('Reached Philosopy!')
        sys.exit(0)

    paragraphs = soup.find_all('p')
    for para in paragraphs:
        para = remove_word_origin(para, title)
        links = para.find_all('a')
        if links:
            first_link = select_link(links, para)
            if not first_link:
                continue

            if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', first_link):
                next_url = first_link
            else:
                next_url = "https://en.wikipedia.org%s" % first_link
            main(next_url, steps)
    else:
        logger.info("No links for this article. Reached dead end. Please try again.")
        sys.exit(0)


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
    main(topic_url, steps=0)

    return req


if __name__ == '__main__':
    topic = input('Please enter a topic name: \n')
    topic = topic.replace(" ", "_")
    topic_url = "https://en.wikipedia.org/wiki/%s" % topic
    logger.info("Initial URL: {}".format(topic_url))
    main(topic_url, steps=0)
