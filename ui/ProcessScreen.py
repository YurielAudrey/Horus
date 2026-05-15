from textual.screen import Screen
from textual import on ,work
from textual.app import App, ComposeResult
from textual.containers import Horizontal,Vertical,Grid
from textual.widgets import Static ,Header,Footer,Rule,Label,Input,Button,Checkbox,SelectionList,DataTable,Log
from core import UiUpdate as uup
from core import engine as e

class ProcessScreen(Screen):
    def __init__(self,qtd,url, cfg, isolation, load=False):
        super().__init__()
        self.qtd = qtd
        self.url = url
        self.cfg=cfg
        self.isolation = isolation
        self.load = load

        self.infos = {
            "Email": self.cfg['email'],
            "Threads": self.cfg['threads'],
            "Isolamento": self.isolation,
            "Path": self.cfg['path'],
            "Url Inicial": self.url,
            "Quantidade": self.qtd,
        }


    CSS_PATH =  "processPage.tcss"
    def compose(self):

        yield Header()
        yield self.lay()
        yield Log(classes="log", auto_scroll=True)
        yield DataTable(classes="table")
        yield Footer()

    #preset de parte da interface
    def lay(self)-> Vertical:
        items = []

        items.append(Horizontal(Label("Informações"),
                                classes="infoTitle"))
        for label, value in self.infos.items():
            items.append(Rule(orientation="horizontal",
                              line_style="solid",
                              classes="RuleSeparador"))

            items.append(self.presetInfo(label, value))

        items.append(Rule(orientation="horizontal",
                          line_style="solid",
                          classes="RuleSeparador"))

        return Vertical(*items, classes="verticalConfig")


    #presente de um horizontal com label dentro
    def presetInfo(self,name:str,info) -> Horizontal:

        return Horizontal(Label(name, classes="ILabel"),Label(f"{info}"),classes="ILabel")

    # cria as colunas e linhas da tabela
    def on_mount(self)->None:
        table = self.query_one(DataTable)
        table.add_column("Type", key="type")
        table.add_column("Concluida", key="ok")
        table.add_column("Restante", key="rest")
        table.add_column("Total", key="total")


        table.add_row("URL", "0", "0", "0", key="row_url")
        table.add_row("IMG", "0", "0", "0", key="row_img")
        table.add_row("VID", "0", "0", "0", key="row_vid")
        table.add_row("TEXT", "0", "0", "0", key="row_txt")
        self.start_run()

    #inicializa o engine
    @work(thread=True)
    def start_run(self):
        title = "Horus"
        version = "1.0"


        ua =   {'User-Agent': f"{title}/{version} (https://github.com/YurielAudrey/Horus; {self.cfg['email']}) Request/2.32.5"}

        def update_ui(p, r, t,m):
            self.post_message(uup.UiUpdate(p, r, t,m))

        engine_inst = e.engine(self.url, self.cfg, self.isolation, self.load, ua, update_ui)
        engine_inst.start()


    @on(uup.UiUpdate)
    #atualiza as informacoes da interface
    def atualizar_labels(self, message: uup.UiUpdate):
        log = self.query_one(Log)
        tipos = {
            'urls': 'row_url',
            'imgs': 'row_img',
            'vids': 'row_vid',
            'txt': 'row_txt'
        }

        for i in message.log:
            log.write(f"{i}\n")

        for key_engine, key_tabela in tipos.items():
            table = self.query_one(DataTable)
            valor_concluido = len(message.concluida.get(key_engine, []))
            valor_pendente = message.pendente.get(key_engine, 0)
            valor_total = message.total.get(key_engine, 0)
            table.update_cell(key_tabela, "ok", str(valor_concluido))
            table.update_cell(key_tabela, "rest", str(valor_pendente))
            table.update_cell(key_tabela, "total", str(valor_total))