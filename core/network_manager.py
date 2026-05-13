from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup as s
from urllib.parse import urlparse
from core import parser_utils as pu
from pathlib import Path


def verify_robot(url_inicial ,session,url,ua,isolation):
    ui = urlparse(url_inicial)
    parsed_url = urlparse(url)
    site_map = []
    #caso a opcao isolamento esteja ativada , ele verifica se o url atual e do mesmo site da url inicial
    #para evitar que ele saia rodando em sites com direitos autorais, ou com conteudo indejesado
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
        return cd,rr, permission, site_map
    else:
        site_map.append(f'{parsed_url.scheme}://{parsed_url.netloc}')
        return 0 , 0 , True, site_map

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
    return page_clear,img_clear

def find_name(url: str) -> str:
    parsed_url = urlparse(url)
    path_file = parsed_url.path
    name_file = Path(path_file).name
    return name_file

