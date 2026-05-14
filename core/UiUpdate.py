from textual.message import Message

class UiUpdate(Message):
    def __init__(self,concluida:dict,pendente:dict,total:dict,msg:list[str]):

        self.concluida = concluida
        self.pendente = pendente
        self.total = total
        self.log = msg

        super().__init__()

