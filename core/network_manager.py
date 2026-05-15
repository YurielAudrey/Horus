from bs4 import BeautifulSoup as s
from urllib.parse import urlparse
from core import utils as pu
from pathlib import Path
from protego import Protego
'''
    
'''

#verifica o Robot verificando sites proibidos , Site Map ,crawl delay , request rate

#site map - crawl delay - log - permission
def verify_robot(url_inicial ,session,url,header,isolation):


    ui = urlparse(url_inicial)
    parsed_url = urlparse(url)
    ua = header['User-Agent']
    base_url = f'{parsed_url.scheme}://{parsed_url.netloc}/robots.txt'
    response = session.get(base_url,headers = header)
    code =response.status_code
    rp = Protego.parse(response.text)
    permission = rp.can_fetch(url,ua)
    cd = rp.crawl_delay(ua)
    rr = rp.request_rate(ua)
    if isolation:
        if parsed_url.netloc != ui.netloc:
            msg = f"[WARN] Sistema de Isolamento bloqueou a saida para sites diferente do inicial"
            return url,msg ,0, 0, False,code

    if permission:
        msg = f"[INFO] Permissao Concedida para o Site {url}"
        return url,msg , cd,rr,permission,code
    else:
        msg = f"[WARN] Permissao Negada para o Site {url}"
        return url, msg , cd , rr , permission ,code


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
    msg = f"[INFO] adcionando {len(page_clear)} URLS e {len(img_clear)} Arquivos"
    return msg, page_clear,img_clear

#Captura o nome do arquivo
def find_name(url: str) -> str:
    parsed_url = urlparse(url)
    path_file = parsed_url.path
    name_file = Path(path_file).name
    return name_file


