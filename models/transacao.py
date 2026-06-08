from enum import Enum

class TipoTransacao(Enum):
    RECEITA = "receita"
    DESPESA = "despesa"

class Transacao:
    def __init__(self, tipo: TipoTransacao, descricao: str, valor:float, data:str, categoria:str):
        
        if valor <= 0:
            raise ValueError("Valor deve ser positivo!")
        
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria
        
    def __str__(self):
        emoji = "✅" if self.tipo == TipoTransacao.RECEITA else "❌"
        return f"{emoji} Data: [{self.data}] | Descrição: {self.descricao} | Valor: R$ {self.valor} | Categoria : ({self.categoria})"