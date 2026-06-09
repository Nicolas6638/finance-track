from datetime import datetime
from enum import Enum


class TipoTransacao(Enum):
    RECEITA = "receita"
    DESPESA = "despesa"


class Transacao:
    def __init__(self, tipo: TipoTransacao, descricao: str, valor: float, data: str, categoria: str):
        if valor <= 0:
            raise ValueError("Valor deve ser positivo!")

        if not descricao or not descricao.strip():
            raise ValueError("Descrição não pode ser vazia!")

        if not categoria or not categoria.strip():
            raise ValueError("Categoria não pode ser vazia!")

        datetime.strptime(data, "%d/%m/%Y")

        self.tipo = tipo
        self.descricao = descricao.strip()
        self.valor = valor
        self.data = data
        self.categoria = categoria.strip()
        
    def __str__(self):
        emoji = "✅" if self.tipo == TipoTransacao.RECEITA else "❌"
        return f"{emoji} Data: [{self.data}] | Descrição: {self.descricao} | Valor: R$ {self.valor} | Categoria : ({self.categoria})"