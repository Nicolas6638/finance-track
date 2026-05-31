from models.transacao import Transacao

class Receita(Transacao):
    def __init__(self, descricao, valor, data, categoria):
        super().__init__(descricao, valor, data, categoria)