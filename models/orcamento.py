from datetime import datetime

class Orcamento:
    def __init__(self, categoria: str, mes: str, limite: float):
        
        if not categoria:
            raise ValueError("A categoria não pode ser vazia")
        
        if not mes or not mes.strip():
            raise ValueError("O mês/ano não pode ser vazio.")
        
        try:
            datetime.strptime(mes, "%m/%Y")
        
        except ValueError:
            raise ValueError(f"O mês '{mes}' é inválido, use o formato MM")
        
        if limite <= 0:
            raise ValueError("Limite deve ser positivo!")
        
        self.categoria = categoria.strip()
        self.mes = mes.strip()
        self.limite = limite
        

    def __str__(self):
        
        return f"Categoria: [{self.categoria}] | Mês: {self.mes} | Limite: R$ {self.limite}"