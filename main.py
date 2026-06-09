from models.carteira import Carteira
from models.transacao import Transacao, TipoTransacao
from database.conexao import criar_tabela


carteira = Carteira()

def formatar_transacao(t):
    id_, tipo, descricao, valor, categoria, data = t
    emoji = "✅" if tipo == "receita" else "❌"
    return f"ID: {id_} | {emoji} {descricao} | R$ {valor:.2f} | {categoria} | {data}"

def ler_float(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("⚠️ Valor inválido ! Digite um número.")

def ler_int(mensagem):           
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("⚠️ Número inválido!")

def opcao_listar():
    transacao = carteira.listar()
    
    if not transacao:
        print("Nenhuma transação encontrada.")
        return
    for t in transacao:
        print(formatar_transacao(t))
 
 
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
        
def main():
    criar_tabela()
while True:

    opcao  = ler_int("Escolha a opção: ")
    print()
    
    match opcao:
        case 1:
            t = Transacao(
                TipoTransacao.RECEITA, input("Descrição: "), ler_float("Valor: "), input("Data (DD/MM/AAAA): "), input("Categoria: "))
            carteira.adicionar_transacao(t)
            print("✅ Receita adicionada!")
            
        case 2:
            t = Transacao(
                TipoTransacao.DESPESA, input("Descrição: "), ler_float("Valor: "), input("Data (DD/MM/AAAA): "), input("Categoria: "))
            carteira.adicionar_transacao(t)
            print("✅ Despesa adicionada!")
            
            
        case 3:
            carteira.listar()
            
        case 4:
            id_ = ler_int("Digite o id para deletar: ")
            carteira.deletar(id_)
            print(f"🗑️ Transação {id_} deletada com sucesso!")
            
        case 5:
            categoria = input("Digite a categoria: ")
            transacoes = carteira.filtrar_categoria(categoria)
            if not transacoes:
                print(f"⚠️ Nenhuma transação na categoria: {categoria}")
            
            else:
                for t in transacoes:
                    print(formatar_transacao(t))
            
        case 6:
            resumo = carteira.resumo()
            if not resumo:
                print("⚠️ Nenhuma despesa registrada.")
            else:
                print("📊 Resumo de gastos por categoria:")
                for r in resumo:
                        print(f"🔸 {r[0]}: R$ {r[1]}")
            
        case 7:
            print(f"💰 Saldo atual: R${carteira.calcular_saldo()}")
            
        case 8:
            opcao_listar()
            print()
            tipo = input("Novo tipo (receita/despesa): ")
            id_ = ler_int("Digite o id da transção: ")
            
            descricao = input("Nova descrição: ")
            valor = float(input("Novo valor: "))
            data = input("Nova data: ")
            categoria = input("Nova categoria: ")
            
            
            carteira.editar(id_transacao=id_, TipoTransacao=tipo,descricao=descricao, valor=valor, data=data, categoria=categoria)
            print(f"✏️ Transação {id_} editada com sucesso!")
            
        case 9:
            mes = input("Informe o mêS (MM/AAAA): ")
            transacao = carteira.filtrar_mes(mes)
            
            if not transacao:
                print(f"⚠️ Nenhuma transação encontrada para {mes}.")
            else:
                for t in transacao:
                    print(formatar_transacao(t))
        
        case 10:
            carteira.exportar_csv()
            print("📁 Relatório exportado com sucesso: relatorio.csv")
        case 0:
            print("Até logo! 👋")
            
        
if __name__ == "__main__":
    main()