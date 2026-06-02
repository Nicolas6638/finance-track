from models.despesa import Despesa
from models.receita import Receita
from models.carteira import Carteira
from database.conexao import criar_tabela
from database.repositorio import salvar_transacao, listar_transacoes

carteira = Carteira()
# carteira.adicionar_transacao(Despesa("PlaySatition Plus", 450, "1/06/2026", "Jogos"))
carteira.listar()
carteira.deletar(2)
carteira.listar()