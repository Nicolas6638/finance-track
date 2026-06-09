from database.conexao import criar_tabela
from models.carteira import Carteira
from models.transacao import Transacao, TipoTransacao
import tkinter as tk

criar_tabela()
carteira = Carteira()

janela = tk.Tk()
janela.title("💰 Organizador Financeiro")
janela.geometry("600x400")

label = tk.Label(janela, text="💰 Organizador Financeiro", font=("Arial", 18, "bold"))
label.pack(pady=20)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

frame_resultado = tk.LabelFrame(janela, text="📋 Resultados", padx=10, pady=10)
frame_resultado.pack(pady=10, padx=20, fill="both", expand=True)

frame_texto = tk.Frame(frame_resultado)
frame_texto.pack(fill="both", expand=True)

texto_resultado = tk.Text(frame_texto, height=10, width=70)
scrollbar = tk.Scrollbar(frame_texto, orient="vertical", command=texto_resultado.yview)
texto_resultado.configure(yscrollcommand=scrollbar.set)
texto_resultado.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def exibir(mensagem):
    texto_resultado.insert(tk.END, mensagem + "\n")
    texto_resultado.see(tk.END)

def formatar_transacao(t):
    id_, tipo, descricao, valor, categoria, data = t
    emoji = "✅" if tipo == "receita" else "❌"
    return f"ID: {id_} | {emoji} {descricao} | R$ {valor:.2f} | {categoria} | {data}"

def listar_transacoes_gui():
    texto_resultado.delete("1.0", tk.END)
    transacoes = carteira.listar()
    if not transacoes:
        exibir("Nenhuma transação encontrada.")
        return
    for t in transacoes:
        exibir(formatar_transacao(t))

def ver_saldo_gui():
    texto_resultado.delete("1.0", tk.END)
    exibir(f"💰 Saldo atual: R$ {carteira.calcular_saldo():.2f}")

def resumo_categoria_gui():
    texto_resultado.delete("1.0", tk.END)
    resumo = carteira.resumo()
    if not resumo:
        exibir("Nenhuma despesa registrada.")
        return
    exibir("📊 Resumo de gastos por categoria:")
    for r in resumo:
        exibir(f"🔸 {r[0]}: R$ {r[1]}")

tk.Button(frame_botoes, text="📋 Listar Transações", width=25, command=listar_transacoes_gui).pack(pady=5)
tk.Button(frame_botoes, text="💰 Ver Saldo", width=25, command=ver_saldo_gui).pack(pady=5)
tk.Button(frame_botoes, text="📊 Resumo por Categoria", width=25, command=resumo_categoria_gui).pack(pady=5)
tk.Button(frame_botoes, text="❌ Sair", width=25, command=janela.destroy).pack(pady=5)

# --- Formulário ---
frame_form = tk.LabelFrame(janela, text="Nova Transação", padx=10, pady=10)
frame_form.pack(pady=10, padx=20, fill="x")

tk.Label(frame_form, text="Descrição:").grid(row=0, column=0, sticky="w")
entry_descricao = tk.Entry(frame_form, width=30)
entry_descricao.grid(row=0, column=1, padx=5)

tk.Label(frame_form, text="Valor:").grid(row=1, column=0, sticky="w")
entry_valor = tk.Entry(frame_form, width=30)
entry_valor.grid(row=1, column=1, padx=5)

tk.Label(frame_form, text="Data (DD/MM/AAAA):").grid(row=2, column=0, sticky="w")
entry_data = tk.Entry(frame_form, width=30)
entry_data.grid(row=2, column=1, padx=5)

tk.Label(frame_form, text="Categoria:").grid(row=3, column=0, sticky="w")
entry_categoria = tk.Entry(frame_form, width=30)
entry_categoria.grid(row=3, column=1, padx=5)

def limpar_campos():
    entry_descricao.delete(0, tk.END)
    entry_valor.delete(0, tk.END)
    entry_data.delete(0, tk.END)
    entry_categoria.delete(0, tk.END)

def adicionar_transacao_gui(tipo):
    try:
        valor = float(entry_valor.get().replace(",", "."))
    except ValueError:
        exibir("⚠️ Valor inválido! Digite um número.")
        return

    transacao = Transacao(tipo, entry_descricao.get(), valor, entry_data.get(), entry_categoria.get())
    carteira.adicionar_transacao(transacao)
    exibir(f"✅ {tipo.value.capitalize()} adicionada!")
    limpar_campos()

tk.Button(frame_form, text="✅ Adicionar Receita", command=lambda: adicionar_transacao_gui(TipoTransacao.RECEITA)).grid(row=4, column=0, pady=10)
tk.Button(frame_form, text="❌ Adicionar Despesa", command=lambda: adicionar_transacao_gui(TipoTransacao.DESPESA)).grid(row=4, column=1, pady=10)

if __name__ == "__main__":
    janela.mainloop()