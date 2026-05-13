def fix_url(scheme,netloc ,u):
    url = u
    if url.startswith('https://'):
        return url
    else:
        return f'{scheme}://{netloc}/{url}'




