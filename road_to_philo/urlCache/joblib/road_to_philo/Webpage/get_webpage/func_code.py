# first line: 15
@memory.cache
def get_webpage(url):
    logger.debug("Cache not used")
    r = requests.get(url)
    return r
