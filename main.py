from models.despesa import Despesa
from models.receita import Receita
from models.carteira import Carteira
from database.conexao import criar_tabela
from database.repositorio import salvar_transacao, listar_transacoes, buscar_por_categoria
import time

carteira = Carteira()

def menu():
    print("""
==========================
  💰 Organizador Financeiro
==========================
1. Adicionar Receita
2. Adicionar Despesa
3. Listar Transações
4. Deletar Transação
5. Filtrar por Categoria
6. Resumo por Categoria
7. Ver Saldo
8. Editar Transação
9. Filtra por Mês
10. Exportar Relatório CSV
0. Sair
==========================      
          
          """)
    
while True:
    menu()
    
    opcao  = int(input("Escolha a opção: "))
    print()
    
    match opcao:
        case 1:
            descricao = input("Descrição: ")
            valor = float(input("Valor: "))
            data = input("Data (DD/MM/AAAA): ")
            categoria = input("Categoria: ")
            carteira.adicionar_transacao(Receita(descricao=descricao, valor=valor, data=data, categoria=categoria))
            print("✅ Receita adicionada!")
        
        case 2:
            descricao = input("Descrição: ")
            valor = float(input("Valor: "))
            data = input("Data (DD/MM/AAAA): ")
            categoria = input("Categoria: ")
            carteira.adicionar_transacao(Despesa(descricao=descricao, valor=valor, data=data, categoria=categoria))
            print("✅ Receita adicionada!")
            
        case 3:
            carteira.listar()
            
        case 4:
            carteira.deletar()
            id = int(input("Digite o id para deletar: "))
            carteira.deletar(id)
            
        case 5:
            categoria = input("Digite a categoria: ")
            carteira.filtrar_categoria(categoria)
            
        case 6:
            carteira.resumo()
            
        case 7:
            carteira.calcular_saldo()
            
        case 8:
            carteira.listar()
            print()
            
            id = int(input("Digite o id da transção: "))
            descricao = input("Informe a nova descrição: ")
            valor = float(input("Informe o novo valor: "))
            data = input("Informe a nova data: ")
            categoria = input("Informe a nova categoria: ")
            
            print()
            carteira.editar(id=id, descricao=descricao, valor=valor, data=data, categoria=categoria)
        
        case 9:
            mes = input("Informe a data nesse formarto (MM/AAAA): ")
            print()
            carteira.filtrar_mes(mes)
        
        case 10:
            carteira.exportar_csv()
            
            time.sleep(1.5)
            print("📁 Relatório exportado com sucesso: relatorio.csv")
            time.sleep(0.5)
        case 0:
            print("Até logo! 👋")
            break