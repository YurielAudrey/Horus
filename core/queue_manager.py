import queue
import threading
import time


class queue_manager:
    def __init__(self):
        self.crawl_delay = 0
        self.request_rate = 0
        self.page_queue = queue.Queue()
        self.img_queue = queue.Queue()
        self.vid_queue = queue.Queue()
        self.txt_queue = queue.Queue()
        self.last_request = 0
        self.lock= threading.Lock()

    def queue_to_list(self):
        u = []
        d = []
        for i in range(self.page_queue.qsize()):
            url = self.get_url()
            u.append(url)

        for i in range(self.img_queue.qsize()):
            down = self.get_img()
            d.append(down)

        return u,d


    def put_item(self,**kwargs):


        page_list = kwargs.get('page_list',[])
        down_list = kwargs.get('down_list',[])

        if len(page_list)>0 :
            for u in page_list:
                self.page_queue.put(u)

        if len(down_list)>0 :
            for u in down_list:
                self.img_queue.put(u)

    def delay_counter(self) -> None:
        while True:
            with self.lock:
                agora = time.perf_counter()
                t = agora-self.last_request
                bl =t >= self.crawl_delay
                if bl:
                    self.last_request = time.perf_counter()
                    return
            time.sleep(0.1)



    def get_url(self):
        self.delay_counter()

        item = self.page_queue.get()
        return item


    def get_img(self):
        self.delay_counter()
        item = self.img_queue.get()
        return item

    def get_vid(self):
        self.delay_counter()
        item = self.vid_queue.get()
        return item

    def get_txt(self):
        self.delay_counter()
        item = self.txt_queue.get()
        return item
