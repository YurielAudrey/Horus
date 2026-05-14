from datetime import datetime
from rich.text import Text

def fix_url(scheme,netloc ,u):
    url = u
    if url.startswith('https://'):
        return url
    else:
        return f'{scheme}://{netloc}/{url}'

def log_Manager(msg:str):

    timestamp = datetime.now().strftime("%H:%M:%S")
    txt =Text.assemble(
        (f"{timestamp} ","dim"),
        (msg,"bold magenta")
    )
    return txt

