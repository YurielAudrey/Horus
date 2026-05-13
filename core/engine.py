import requests
from urllib.parse import urlparse
from rich.live import Live
from ui import ProcessScreen as lm
import core.network_manager as nm
import core.thread_manager as tm
import core.queue_manager as qm
import core.storage_handler as sh


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


        self.stats_data = set()

    def start(self) -> None:


        crawl_delay, request_rate, _, site_map = nm.verify_robot(self.url_inicial,
                                                                 self.session,
                                                                 self.url_inicial,
                                                                 self.ua,
                                                                 self.isolation)

        qm.crawl_delay = crawl_delay
        qm.request_rate = request_rate

        if self.load:

            self.queue.put_item(page_list=sh.load_url(self.cfg["path"],"utf-8"),
                                down_list=sh.load_url(self.cfg["path"],"utf-8"))
        else:
            self.queue.put_item(page_list=site_map)

        self.t.create_threads(func=self.manager_list,
                              list_thr=self.t.thr_url,
                              name = "tu_",
                              )

        self.t.create_threads(func=self.download,
                              list_thr=self.t.thr_down,
                              name="td_",
                              path = self.cfg["path"]
                              )


        self.t.start_thr()

        self.t.join_thr()

    def manager_list(self,**kwargs) -> None:
        live = kwargs.get('live')
        while True:
            url= self.queue.get_url()
            if self.callback:
                c,p,t = self.att_var()
                self.callback(c,p,t)
            _, _, permission, _ = nm.verify_robot(self.url_inicial,
                                                  self.session,
                                                  url,
                                                  self.cfg["user-agent"],
                                                  self.isolation)
            if permission:
                up = urlparse(url)
                html = self.session.get(url, headers=self.cfg["user-agent"])
                page_new, down_new = nm.get_url(up.scheme, up.netloc, html)
                self.queue.put_item(page_list=page_new,down_list=down_new)
                down_new.clear()
                page_new.clear()
                self.page_old.append(url)

                if self.queue.page_queue.qsize() == 0:
                    break



    def download(self,**kwargs) -> None :
        path = kwargs['path']
        while True:
            url = self.queue.get_img()
            name_file = nm.find_name(url)
            response = self.session.get(url,headers = self.cfg["user-agent"])
            sh.save_file(name_file,path,response)

            self.img_old.append(url)
            if self.queue.img_queue.qsize()==0:
                break

    def att_var(self):
        concluida = {
            'urls': self.page_old,
            'imgs': self.img_old,
            'vids': self.vid_old,
            'txt': self.txt_old,
        }
        pendente = {
            'urls': self.queue.get_url(),
            'imgs': self.queue.get_img(),
            'vids': self.queue.get_vid(),
            'txt': self.queue.get_txt(),
        }

        total = {
            'urls': len(self.page_old)+self.queue.page_queue.qsize(),
            'imgs': len(self.img_old)+self.queue.img_queue.qsize(),
            'vids': len(self.vid_old)+self.queue.vid_queue.qsize(),
            'txt': len(self.txt_old)+self.queue.txt_queue.qsize(),
        }
        return concluida,pendente,total


