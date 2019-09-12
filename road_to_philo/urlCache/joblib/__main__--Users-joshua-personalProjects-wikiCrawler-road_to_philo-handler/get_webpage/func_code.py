# first line: 60
@memory.cache
def get_webpage(url):
    logger.debug("Cache not used")
    r = requests.get(url)
    status_code = r.status_code
    if status_code == 404:
        return r, False
    else:
        return r, True
