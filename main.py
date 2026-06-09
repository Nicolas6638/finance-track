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
            print("⚠️ Valor inválido! Digite um número.")


def ler_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("⚠️ Número inválido!")


def opcao_listar():
    transacoes = carteira.listar()
    if not transacoes:
        print("Nenhuma transação encontrada.")
        return
    for t in transacoes:
        print(formatar_transacao(t))


def main():
    criar_tabela()
    while True:
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
9. Filtrar por Mês
10. Exportar Relatório CSV
0. Sair
==========================
        """)

        opcao = ler_int("Escolha a opção: ")
        print()

        match opcao:
            case 1:
                t = Transacao(
                    TipoTransacao.RECEITA, input("Descrição: "),
                    ler_float("Valor: "),
                    input("Data (DD/MM/AAAA): "),
                    input("Categoria: "))
                carteira.adicionar_transacao(t)
                print("✅ Receita adicionada!")

            case 2:
                t = Transacao(
                    TipoTransacao.DESPESA, input("Descrição: "),
                    ler_float("Valor: "),
                    input("Data (DD/MM/AAAA): "),
                    input("Categoria: "))
                carteira.adicionar_transacao(t)
                print("✅ Despesa adicionada!")

            case 3:
                opcao_listar()

            case 4:
                id_ = ler_int("Digite o id para deletar: ")
                if carteira.deletar(id_):
                    print(f"🗑️ Transação {id_} deletada com sucesso!")
                else:
                    print(f"⚠️ Transação {id_} não encontrada.")

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
                print(f"💰 Saldo atual: R$ {carteira.calcular_saldo():.2f}")

            case 8:
                opcao_listar()
                print()
                id_ = ler_int("Digite o id da transação: ")
                tipo = input("Novo tipo (receita/despesa): ")
                descricao = input("Nova descrição: ")
                valor = ler_float("Novo valor: ")
                data = input("Nova data: ")
                categoria = input("Nova categoria: ")
                carteira.editar(id_, tipo, descricao, valor, data, categoria)
                print(f"✏️ Transação {id_} editada com sucesso!")

            case 9:
                mes = input("Informe o mês (MM/AAAA): ")
                transacoes = carteira.filtrar_mes(mes)
                if not transacoes:
                    print(f"⚠️ Nenhuma transação encontrada para {mes}.")
                else:
                    for t in transacoes:
                        print(formatar_transacao(t))

            case 10:
                carteira.exportar_csv()
                print("📁 Relatório exportado: relatorio.csv")

            case 0:
                print("Até logo! 👋")
                break


if __name__ == "__main__":
    main()