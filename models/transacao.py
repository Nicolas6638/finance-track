class Transacao:
    def __init__(self, descricao, valor, data, categoria):
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria
        
    def __str__(self):
        return f"Data: [{self.data}] | Descrição{self.descricao} | Valor: R$ {self.valor} | Categoria : ({self.categoria})"