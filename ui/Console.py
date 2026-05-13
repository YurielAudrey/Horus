from textual import on ,work
from textual.app import App, ComposeResult
from textual.containers import Horizontal,Vertical
from textual.widgets import Static ,Header,Footer,Rule,Label,Input,Button,Checkbox,SelectionList
import core.storage_handler as sh
from core import engine as e

from textual.screen import Screen
from ui.ProcessScreen import ProcessScreen

class ui(App):

    TITLE = "Horus 1.0"
    CSS_PATH = "layout.tcss"
    BINDINGS =[
            ("ctrl+s","save_quit","salvar e fechar"),
            ("ctrl+p","pause","pausar"),
    ]
    SCREENS = {
        "settings": ProcessScreen,
    }

    def compose(self) -> ComposeResult:
        yield Header(name="Horus", show_clock=True, classes="header")
        yield Horizontal(
            Vertical(
                Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                Static("Run", classes="titleLabel_cfg"),
                Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),

                Horizontal(
                    Label("URL", classes="label_cfg"),
                    Input(placeholder="Entre com a URL", classes="input_cfg", type="text", id="url_input"),
                    Horizontal(
                        Label("Quant.", classes="label_cfg"),
                        Input(placeholder="", classes="input_cfg var1", type="number", id="qtd_input"),
                        classes="horizontalSmall"
                    ),
                    classes="vertical_cfg"
                ),
                Horizontal(
                    Checkbox("Load", classes="Check", id="load_check"),
                    Checkbox("Isolar", classes="Check", id="isola_check"),

                    classes="vertical1"
                )
                ,
                Horizontal(classes="gambiarra"),  # mudar
                Button("RUN", classes="ButtonRun", id="run")
            ),

            Rule(orientation="vertical", line_style="solid", classes="RuleSeparador"),

            Vertical(
                Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),
                Static("Configuracao", classes="titleLabel_cfg"),
                Rule(orientation="horizontal", line_style="solid", classes="RuleSeparador"),

                Horizontal(
                    Label("Email", classes="label_cfg"),
                    Input(placeholder="", classes="input_cfg", type="text", id="email_input"),
                    classes="vertical_cfg"

                ),
                Horizontal(
                    Label("Threads", classes="label_cfg"),
                    Input(placeholder="", classes="input_cfg var1", type="number", id="threads_input"),
                    classes="vertical_cfg",

                ),
                Horizontal(
                    Label("Path", classes="label_cfg"),
                    Input(placeholder="", classes="input_cfg", type="text", id="path_input"),
                    classes="vertical_cfg",

                ),
                Horizontal(
                    Horizontal(classes="gambiarra"),  # mudar
                    SelectionList[bool](
                        ("Imagem", "img", False),
                        ("Video", "vid", False),
                        ("Texto", "txt", False),
                        ("Tudo", "all", False),
                        classes="listCheck",
                        id="types"

                    ),
                    Horizontal(classes="gambiarra"),  # mudar
                ),
                Horizontal(classes="gambiarra"),  # mudar
                Button("Salvar Configuracao", classes="ButtonRun", id="config"),

            )
        )

        yield Footer(name="Footer")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "config":
            email = self.query_one("#email_input", Input).value
            threads = self.query_one("#threads_input", Input).value
            path = self.query_one("#path_input", Input).value
            list_selection = self.query_one("#types", SelectionList)
            img = False
            vid = False
            txt = False
            all_opx = False
            for i in list_selection.selected:
                if i == "img":
                    img = True
                if i == "vid":
                    vid = True
                if i == "txt":
                    txt = True
                if i == "all":
                    all_opx = True

            sh.save_cfg(threads=threads,
                        email=email,
                        path=path,
                        img=img,
                        videos=vid,
                        text=txt,
                        all=all_opx)

        if event.button.id == "run":
            url = self.query_one("#url_input", Input).value
            cfg, _ = sh.load_cfg()
            isolation = self.query_one("#isola_check", Checkbox).value
            load = self.query_one("#isola_check", Checkbox).value
            screen = ProcessScreen(url,cfg,isolation,load)
            self.push_screen(screen)



    def action_save_quit(self) -> None:
        self.exit()

    def action_pause(self) -> None:
        pass


