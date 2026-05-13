from textual.message import Message

class UiUpdate(Message):
    def __init__(self,concluida:dict,pendente:dict,total:dict):

        self.concluida = concluida
        self.pendente = pendente
        self.total = total

        self.total = total
        super().__init__()

