from rich.layout import Layout
from rich.table import Table
style_1 = "bold green"
layout = Layout()

class personalL:
    def __init__(self,data):
        self.list_column = ["desc","qtd","total","porcent","fails","imagens"]
        self.data = data
        self.create_table(data)

    def create_table(self,data):
        table = Table(expand=True)
        for column in self.list_column:
            table.add_column(column, justify="center", style=style_1)
        table = self.create_row(table,data)
        return table

    def create_row(self, table ,data):
        for x in range(len(data)):
            table.add_row(
                data[x]["descricao"], str(data[x]["QTD"]),
                str(data[x]["Total"]),f"{data[x]["%"]: .2f}%",
                str(data[x]["fails"]),str(data[x]["imagens"])
            )
        return table






