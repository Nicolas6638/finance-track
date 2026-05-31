from models.transacao import Transacao
from models.receita import Receita
from database.conexao import criar_tabela

criar_tabela()

print("Banco de dados criado com sucesso!")