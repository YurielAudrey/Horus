import requests
from urllib.parse import urlparse
from rich.live import Live
from ui import ProcessScreen as lm
import core.network_manager as nm
import core.thread_manager as tm
import core.queue_manager as qm
import core.storage_handler as sh
from datetime import datetime
import core.utils as u


column = ["desc","Concluidas","Restante","total","Loading"]
class engine:
    def __init__(self,url:str, config:dict, isolation:bool, load:bool,ua,callback_func=None):
        self.callback = callback_func
        self.load =load
        self.session = requests.Session()
        self.cfg = config
        self.isolation = isolation
        self.ua = ua
        self.url_inicial = url
        self.t = tm.threads(self.cfg['threads'])
        self.queue = qm.queue_manager()
        self.page_old = []
        self.img_old = []
        self.vid_old = []
        self.txt_old = []
        self.log_cache=[]
        self.stats_data = set()


    #regula o delay entre requisicoes caso retorne code 429
    def request_code_manager(self,code:int):
        if code == 429:
            self.queue.add_delay(1)
            self.add_log("[WARN]Requisicao Bloqueada pelo site Por excesso de requisicoes")

    def add_log(self,text:str)->None:
        self.log_cache.append(
                u.log_Manager(text)
        )

    #inicia o codigo principal do scrapper
    def start(self) -> None:
        self.add_log("[INFO]Engine Iniciada ")

        url,msg , crawl_delay , request_rate , permission , code = nm.verify_robot(
                                                self.url_inicial,self.session,
                                                self.url_inicial,self.ua, self.isolation)

        self.queue.put_item(page_list=[url])

        self.log_cache.append(msg)
        self.request_code_manager(code)
        qm.crawl_delay = crawl_delay
        qm.request_rate = request_rate
        if self.load:
            self.add_log("[INFO]Carregando Urls Salvas")
            self.queue.put_item(page_list=sh.load_url(self.cfg["path"],"utf-8"),
                                down_list=sh.load_url(self.cfg["path"],"utf-8"))
        self.t.create_threads(func=self.manager_list , list_thr=self.t.thr_url,name = "tu_",)
        self.t.create_threads(func=self.download,list_thr=self.t.thr_down,name="td_",path = self.cfg["path"])
        self.t.start_thr()
        self.t.join_thr()

    #comeca capturar as urls
    def manager_list(self,**kwargs) -> None:
        while True:
            url= self.queue.get_url()

            url , msg , _ , _ , permission, code = nm.verify_robot(self.url_inicial,
                                                                  self.session,
                                                                  url,
                                                                  self.ua,
                                                                  self.isolation)

            self.add_log(msg)
            self.request_code_manager(code)
            if permission:
                up = urlparse(url)
                html = self.session.get(url, headers=self.ua)
                msg ,page_new, down_new = nm.get_url(up.scheme, up.netloc, html)
                self.add_log(msg)
                self.queue.put_item(page_list=page_new,down_list=down_new)
                down_new.clear()
                page_new.clear()
                self.page_old.append(url)
                if self.callback:
                    c, p, t = self.att_var()
                    m=self.log_cache
                    self.callback(c, p, t,m)

                if self.queue.page_queue.qsize() == 0:
                    self.add_log("[INFO]Sem Mais Urls para Processar")
                    break


    #realiza o download dos arquivos
    def download(self,**kwargs) -> None :
        path = kwargs['path']
        while True:
            url = self.queue.get_img()
            name_file = nm.find_name(url)
            response = self.session.get(url,headers = self.ua)
            code = response.status_code
            self.request_code_manager(code)
            sh.save_file(name_file,path,response)

            self.img_old.append(url)
            self.add_log(f"[INFO]Arquivo : {name_file} Salvo")
            if self.queue.img_queue.qsize()==0:
                self.add_log("[INFO]Sem Mais Arquivos para baixar")
                break

    #atualiza as variaveis e para enviar para a interface atravez de message do textual
    def att_var(self):
        concluida = {
            'urls': self.page_old,
            'imgs': self.img_old,
            'vids': self.vid_old,
            'txt': self.txt_old,
        }
        pendente = {
            'urls': self.queue.page_queue.qsize(),
            'imgs': self.queue.img_queue.qsize(),
            'vids': self.queue.vid_queue.qsize(),
            'txt': self.queue.txt_queue.qsize(),
        }

        total = {
            'urls': len(self.page_old)+self.queue.page_queue.qsize(),
            'imgs': len(self.img_old)+self.queue.img_queue.qsize(),
            'vids': len(self.vid_old)+self.queue.vid_queue.qsize(),
            'txt': len(self.txt_old)+self.queue.txt_queue.qsize(),
        }
        return concluida,pendente,total


