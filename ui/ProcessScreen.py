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
    CSS_PATH =  "processPage.tcss"
    def compose(self):
        yield Header()


        yield Vertical(
                    Horizontal(
                        Label("Informacoes"),
                        classes="infoLabel"
                    ),
                    Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                    Horizontal(
                        Label("Email:",classes="ILabel"),
                        Label(f"{self.cfg['email']}"),
                        classes="ILabel"
                    ),
                    Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                    Horizontal(
                        Label("Threads:",classes="ILabel"),
                        Label(f"{self.cfg['threads']}"),
                        classes="ILabel"
                    ),
                    Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                    Horizontal(
                        Label("Isolamento:",classes="ILabel"),
                        Label(f"{self.isolation}"),
                        classes="ILabel"
                    ),
                    Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                    Horizontal(
                        Label("Path:",classes="ILabel"),
                        Label(f"{self.cfg['path']}"),
                        classes="ILabel"
                    ),
                    Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                    Horizontal(
                        Label("Url Inicial:",classes="ILabel"),
                        Label(f"{self.url}"),
                        classes="ILabel"
                    ),
                    Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                    Horizontal(
                        Label("Quantidade:",classes="ILabel"),
                        Label(f"{self.qtd}"),
                        classes="ILabel"
                    ),
                    Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                    classes="verticalConfig")
        yield Log(classes="log", auto_scroll=True)
        yield DataTable(classes="table")




        yield Footer()

    def on_mount(self)->None:
        log = self.query_one(Log)
        log.write_line("msg mount")

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

    @work(thread=True)
    def start_run(self):  # Remova o 'async'
        title = "Horus"
        version = "1.0"

        ua = {'User-Agent': f"{title}/{version} (https://github.com/YurielAudrey; {self.cfg['email']})"}

        self.app.call_from_thread(self.query_one(Log).write_line, "msg start")

        def update_ui(p, r, t,m):
            self.post_message(uup.UiUpdate(p, r, t,m))

        engine_inst = e.engine(self.url, self.cfg, self.isolation, self.load, ua, update_ui)
        engine_inst.start()

    @on(uup.UiUpdate)
    def atualizar_labels(self, message: uup.UiUpdate):
        log = self.query_one(Log)
        tipos = {
            'urls': 'row_url',
            'imgs': 'row_img',
            'vids': 'row_vid',
            'txt': 'row_txt'
        }

        for i in message.log:
            try:
                # Se o destino for o widget Log do Textual, ele aceita o objeto Text!
                log.write(i)
            except TypeError:
                # Se der erro, é porque algo no caminho exige string pura
                log.write(f"{str(i.plain)}\n")

        for key_engine, key_tabela in tipos.items():
            table = self.query_one(DataTable)





            valor_concluido = len(message.concluida.get(key_engine, []))
            valor_pendente = message.pendente.get(key_engine, 0)
            valor_total = message.total.get(key_engine, 0)
            table.update_cell(key_tabela, "ok", str(valor_concluido))
            table.update_cell(key_tabela, "rest", str(valor_pendente))
            table.update_cell(key_tabela, "total", str(valor_total))