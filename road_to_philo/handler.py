from bs4 import BeautifulSoup
import requests
import sys
import urllib.parse as urlparse
import re
from os import getenv

visited_pages = []


def main(url, steps):
    steps += 1
    r = requests.get(url)
    if r.status_code == 404:
        print('No such wiki page. Please try another topic.')
        sys.exit(0)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.string.split('-')[0]
    if title not in visited_pages:
        visited_pages.append(title)
    else:
        print('Entered a loop! Back at: {}'.format(title))
        sys.exit(0)
    print('Step number: {} - {}'.format(steps, title))

    if url == 'https://en.wikipedia.org/wiki/Philosophy':
        print('Reached Philosopy!')
        sys.exit(0)

    paragraphs = soup.find_all('p')
    for para in paragraphs:
        links = para.find_all('a')
        if links:
            for link in links:
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
                    break
            else:
                continue

            if re.match(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', first_link):
                next_url = first_link
            else:
                next_url = "https://en.wikipedia.org%s" % first_link
            main(next_url, steps)
    else:
        print("No links for this article. Reached dead end. Please try again.")
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
    print(topic_url)
    main(topic_url, steps=0)

    return req


if __name__ == '__main__':
    topic = input('Please enter a topic name: \n')
    topic = topic.replace(" ", "_")
    topic_url = "https://en.wikipedia.org/wiki/%s" % topic
    print(topic_url)
    main(topic_url, steps=0)
