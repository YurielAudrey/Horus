from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup as s
from urllib.parse import urlparse
from core import utils as pu
from pathlib import Path

#verifica o Robot verificando sites proibidos , Site Map ,crawl delay , request rate
def verify_robot(url_inicial ,session,url,ua,isolation):
    ui = urlparse(url_inicial)
    parsed_url = urlparse(url)
    site_map = []
    if isolation:
        if parsed_url.netloc != ui.netloc:
            return 0,0,False,site_map

    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}/robots.txt'
    rp = RobotFileParser()
    cd = rp.crawl_delay(ua)
    rr = rp.request_rate(ua)
    response = session.get(base_url,headers= ua,stream=True)

    if response.status_code == 200:
        rp.set_url(base_url)
        rp.read()
        permission = rp.can_fetch(ua, url)
        site_map = rp.site_maps()
        msg = pu.log_Manager("[INFO] Adcionando Site Map ao banco de dados")
        return msg, cd,rr, permission, site_map
    else:
        site_map.append(f'{parsed_url.scheme}://{parsed_url.netloc}')
        msg = pu.log_Manager(f"[INFO] adcionando {url} ao banco de dados")
        return msg, 0 , 0 , True, site_map

#captura todas as Url no HTMl
def get_url(scheme,netloc,html):

    page_url = []
    img_url = []
    soup = s(html.text,'html.parser')

    for tag in soup.find_all(['img','a','video']):
        if tag.name == 'a':
            url = tag.get('href')
            tipo = "link"
        elif tag.name=='img':
            url = tag.get('src')
            tipo = "img"
        elif tag.name=='video':
            url = tag.get('src')
            tipo = "img"
        elif tag.name=='text':
            pass


        if url:
            url_fixed = pu.fix_url(scheme, netloc, url)
            if url_fixed == "null": url_fixed = ""

            if tipo == "link":
                page_url.append(url_fixed)
            else:
                img_url.append(url_fixed)

    page_clear = list(set(filter(None, page_url)))
    img_clear = list(set(filter(None, img_url)))
    msg = pu.log_Manager(f"[INFO] adcionando {len(page_clear)} URLS e {len(img_clear)} Arquivos")
    return msg, page_clear,img_clear

#Captura o nome do arquivo
def find_name(url: str) -> str:
    parsed_url = urlparse(url)
    path_file = parsed_url.path
    name_file = Path(path_file).name
    return name_file

