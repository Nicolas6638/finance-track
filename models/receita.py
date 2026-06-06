from models.transacao import Transacao

class Receita(Transacao):
    def __init__(self, descricao, valor, data, categoria):
        super().__init__(descricao, valor, data, categoria)
        self.tipo = "receita"
        
    def __str__(self):
        return f"✅ Data: [{self.data}] | Descrição: {self.descricao} | Valor: R$ {self.valor} | tipo : ({self.tipo})"