import requests
from bs4 import BeautifulSoup as s
from rich import print
from rich.live import Live
import personalL as Lay
import threading as thr
import time
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from urllib.error import URLError, HTTPError

# descobrir como fazer para o thread down_img
#esperar o thread manager list capturar imagens para ele baixar , antes de iniciar
#
#
class ws:
    def __init__(self,url_inicial="",qtd=0):

        self.encode = "utf-8"
        self.url_inicial = url_inicial
        self.page_url = []
        self.list_old = []
        self.img_url = []
        self.img_old = []
        self.qtd = qtd
        self.fails = []
        self.sucess = []

        self.info_data = [
            {"descricao": "Urls",
            "QTD": len(self.list_old) ,
            "Total": len(self.page_url),
            "%": 0.0,
            "fails": len(self.fails),
            "imagens": len(self.img_url)},
            {
            "descricao": "Imagens",
            "QTD": len(self.sucess),
            "Total": len(self.img_url),
            "%": 0.0,
            "fails": len(self.fails),
            "imagens": 0}]

        self.playout = Lay.personalL(self.info_data)

    def att_table(self):
        self.info_data = [
            {"descricao": "Urls",
             "QTD": len(self.list_old),
             "Total": len(self.page_url),
             "%": 0.0,
             "fails": len(self.fails),
             "imagens": len(self.img_url)},
            {
                "descricao": "Imagens",
                "QTD": len(self.sucess),
                "Total": len(self.img_url),
                "%": 0.0,
                "fails": len(self.fails),
                "imagens": 0}]

    def start_new(self,url_inicial,ua):
        permission , site_map = self.verify_robot(url_inicial,ua)
        if len(site_map) <1:
            self.page_url.append(url_inicial)
        else:
            for url in site_map:
                permission , _ = self.verify_robot(url,ua)
                if permission:
                    self.page_url.append(url)
                else :
                    self.page_old.append(url)


        t1 = thr.Thread(target=self.manager_list, args=(ua,))
        t2 = thr.Thread(target=self.down_img)
        #self.manager_list(ua)

        t1.start()
        while len(self.img_url) < 0:
            time.sleep(0.5)
        t2.start()

        t1.join()
        t2.join()



    def verify_robot(self,url,ua):
        parsed_url = urlparse(url)
        base_url = f'{parsed_url.scheme}://{parsed_url.netloc}/robots.txt'
        rp = RobotFileParser()


        response = requests.get(base_url,headers= ua)
        if response.status_code == 200:
            rp.set_url(base_url)
            rp.read()
            permission = rp.can_fetch(ua, url)
            site_map = rp.site_maps()
            return permission, site_map
        else:
            return True, []


    def manager_list(self, ua):
        with Live(self.playout.create_table(self.info_data), refresh_per_second=10, transient=True) as live:
            while len(self.page_url) > 0:
                for url in self.page_url:
                    if url=="":
                        self.page_url.pop(0)
                        pass

                    code,html,page_new,img_new = self.scrapper(url,ua)

                    for u in img_new:
                        self.img_url.append(u)
                        img_new.remove(u)
                    self.list_old.append(url)
                    self.page_url.remove(url)
                    self.att_table()
                    live.update(self.playout.create_table(self.info_data))


    def down_img(self):
        count = 0
        for url in self.img_url:
            print("aoba")
            response = requests.get(url)
            with open(f'IMG/image_{count}',"wb") as f:
                f.write(response.content)
            count +=1
            if(response.status_code != 200): self.fails.append(response.status_code)
            else: self.sucess.append(response.status_code)


    def scrapper(self,url,ua):
        up = urlparse(url)
        code, html = self.get_html(url, ua)
        page_url, img_url = self.get_url(up.scheme,up.netloc,html)
        return code,html,page_url,img_url


    def get_html(self,url,user_agent):
        html = requests.get(url,headers = user_agent)
        code = html.status_code
        return code , html

    #arrumar , ja que isso so fix url proveniente do wikipedia , manter ele de forma generica
    def fix_url(self,scheme,netloc ,u):
        url = u
        if url.startswith('https://'):
            return url
        else:
            return f'{scheme}://{netloc}/{url}'


    #vasculha o html em busca de links , tem q refatorar
    def get_url(self,scheme,netloc,html):

        page_url = []
        img_url = []
        soup = s(html.text,'html.parser')

        for tag in soup.find_all(['img','a']):
            if tag.name == 'a':
                url = tag.get('href')
                tipo = "link"
            else:
                url = tag.get('src')
                tipo = "img"

            if url:
                url_fixed = self.fix_url(scheme, netloc, url)
                if url_fixed == "null": url_fixed = ""

                # Joga na lista certa
                if tipo == "link":
                    page_url.append(url_fixed)
                else:
                    img_url.append(url_fixed)

        page_clear = list(filter(None, page_url))
        img_clear = list(filter(None, img_url))
        return page_clear,img_clear

    #transforma a lista em csv
    def save_url(self,page_url,arquivo):
        with open(arquivo,"w",encoding=self.encode) as f:
            count = 0
            for url in page_url:
                if count == 0: pre_save = url
                else :pre_save = f"{pre_save},{url}"
                count =+ 1
            f.write(f"{pre_save}")
        f.close()

    def load_url(self,arquivo):
        with open(arquivo,"r",encoding=self.encode)as f:
            url_list = f.read().split(",")
        f.close()
        return url_list