from textual.screen import Screen
from textual import on ,work
from textual.app import App, ComposeResult
from textual.containers import Horizontal,Vertical,Grid
from textual.widgets import Static ,Header,Footer,Rule,Label,Input,Button,Checkbox,SelectionList,DataTable,Log
from core import UiUpdate as uup
from core import engine as e

class ProcessScreen(Screen):
    def __init__(self,url, cfg, isolation, load):
        super().__init__()
        self.url = url
        self.cfg=cfg
        self.isolation = isolation
        self.load = load
    CSS_PATH =  "processPage.tcss"
    def compose(self):
        yield Header()

        yield Log(classes="log",auto_scroll=True)
        yield Horizontal(classes="tst")
        yield Log(classes="erros")
        yield DataTable(classes="table")



        yield Footer()

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


    @work(thread=True)
    async def start_run(self):
        title = "Horus"
        version = "1.0"
        ua = {'User-Agent': f'{title}/{version} (https://github.com/YurielAudrey/Web-Scraper; {self.cfg['email']})'}

        def update_ui(p, r, t):
            self.post_message(uup.UiUpdate(p, r, t))

        engine = e.engine(self.url, self.cfg, self.isolation, self.load, self.ua, self.update_ui)
        engine.start()

    @on(uup.UiUpdate)  # Ouve a mensagem que o engine enviou
    def atualizar_labels(self, message: uup.UiUpdate):
        tipos = {
            'urls': 'row_url',
            'imgs': 'row_img',
            'vids': 'row_vid',
            'txt': 'row_txt'
        }
        for key_engine, key_tabela in tipos.items():
            table = self.query_one(DataTable)
            # Concluída: Pegamos o tamanho da lista (len)
            valor_concluido = len(message.concluida.get(key_engine, []))

            # Pendente e Total: Já vêm como números (ou tamanhos) do engine
            valor_pendente = message.pendente.get(key_engine, 0)
            valor_total = message.total.get(key_engine, 0)

            # Atualiza a linha específica da tabela
            # Importante: str() evita erros de renderização no DataTable
            table.update_cell(key_tabela, "ok", str(valor_concluido))
            table.update_cell(key_tabela, "rest", str(valor_pendente))
            table.update_cell(key_tabela, "total", str(valor_total))