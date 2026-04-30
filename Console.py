import os
from rich.align import Align
from rich.prompt import Prompt
import pyfiglet
from rich import print
from rich.panel import Panel
import ws

style_1 = "bold green"

class Console:
    def __init__(self,title,version):
        self.title = title
        self.version = version
        self.ua = {'User-Agent': 'WebScraper/0.1 (https://github.com/YurielAudrey/Web-Scraper; yurielaudrey@gmail.com)'}
        self.url_inicial = "https://books.toscrape.com/"
        self.ws = ws.ws(self.url_inicial,self.ua)
        self.console(title,"1.1")

        #self.layout_test(title,version)
    #mostra o titlulo , tao inutil quanto parece
    def title_show(self,title,version):
        title = pyfiglet.figlet_format(f"{title}", font="roman")
        panel = Panel(
            Align.center(f"[bold green]{title}"),
            subtitle=f"[bold blue]V:{version} | By Yuriel Audrey[/bold blue]",
            border_style=style_1,
            padding=(1, 0)
        )
        print(panel)

    #Funcao principal do console , inutil mas nao dispensavel
    def console(self,t,v):

        self.title_show(t,v)
        print("Digite A opcao")
        print("1-Iniciar Novo")
        print("2-Continuar Anterior")
        print("3-Sair")
        x = "1" #Prompt.ask("Escolha a opcao: ",choices=["1","2","3"])
        os.system('cls')


        if x == "1":
            self.ws.start_new(self.url_inicial,self.ua)
            #print(layout)
        elif x == "2":
            code, page_url, img_url = self.ws.start_save(self.ua)
        elif x == "3":
            info_data = [{"descricao": "Urls", "QTD": 0, "Total": 0, "%": 0.0, "fails": 0, "urls": 0, "imagens": 0},
                         {"descricao": "Imagens", "QTD": 0, "Total": 0, "%": 0.0, "fails": 0, "urls": 0, "imagens": 0}]
            print(info_data)
        else:
            pass
