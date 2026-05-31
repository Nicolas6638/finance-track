from models.transacao import Transacao
from models.receita import Receita


transacao = Transacao(descricao='teste',valor=20, data='31/05/2026', categoria='cartão virtual')

receita = Receita(descricao='Salário',valor=1600, data='31/05/2026', categoria='renda')


print(transacao)

print(receita)