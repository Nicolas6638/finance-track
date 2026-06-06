from models.carteira import Carteira
from models.receita import Receita
from models.despesa import Despesa
import tkinter as tk
import sys
import os
from io import StringIO

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

janela = tk.Tk()
janela.title("💰 Organizador Financeiro")
janela.geometry("600x400")

label = tk.Label(janela, text="💰 Organizador Financeiro", font=("Arial", 18, "bold"))
label.pack(pady=20)

carteira = Carteira()

def capturar_print(func, *args, **kwargs):
    old_stdout = sys.stdout
    sys.stdout = StringIO()
    try:
        func(*args, **kwargs)
        return sys.stdout.getvalue()
    finally:
        sys.stdout = old_stdout

def exibir(mensagem):
    texto_resultado.insert(tk.END, mensagem + "\n")
    texto_resultado.see(tk.END)

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

def listar_transacoes_gui():
    texto_resultado.delete("1.0", tk.END)
    output = capturar_print(carteira.listar)
    exibir(output.strip() if output.strip() else "Nenhuma transação encontrada.")

tk.Button(frame_botoes, text="📋 Listar Transações", width=25, 
          command=listar_transacoes_gui).pack(pady=5)

def ver_saldo_gui():
    texto_resultado.delete("1.0", tk.END)
    output = capturar_print(carteira.calcular_saldo)
    exibir(output.strip() if output.strip() else "💰 Saldo: R$ 0,00")

tk.Button(frame_botoes, text="💰 Ver Saldo", width=25, 
          command=ver_saldo_gui).pack(pady=5)

def resumo_categoria_gui():
    texto_resultado.delete("1.0", tk.END)
    output = capturar_print(carteira.resumo)
    exibir(output.strip() if output.strip() else "Nenhuma despesa registrada.")

tk.Button(frame_botoes, text="📊 Resumo por Categoria", width=25, 
          command=resumo_categoria_gui).pack(pady=5)

tk.Button(frame_botoes, text="❌ Sair", width=25, 
          command=janela.destroy).pack(pady=5)

frame_form = tk.LabelFrame(janela, text="Nova Transação", padx=10, pady=10)
frame_form.pack(pady=10, padx=20, fill="x")

frame_resultado = tk.LabelFrame(janela, text="📋 Resultados", padx=10, pady=10)
frame_resultado.pack(pady=10, padx=20, fill="both", expand=True)

frame_texto = tk.Frame(frame_resultado)
frame_texto.pack(fill="both", expand=True)

texto_resultado = tk.Text(frame_texto, height=10, width=70)
scrollbar = tk.Scrollbar(frame_texto, orient="vertical", command=texto_resultado.yview)
texto_resultado.configure(yscrollcommand=scrollbar.set)

texto_resultado.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

tk.Label(frame_form, text="Descrição: ").grid(row=0, column=0, sticky="w")
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

def adicionar_receita():
    try:
        valor = float(entry_valor.get().replace(",", "."))
    except ValueError:
        exibir("⚠️ Valor inválido! Digite um número.")
        return

    carteira.adicionar_transacao(Receita(
        entry_descricao.get(),
        valor,
        entry_data.get(),
        entry_categoria.get()
    ))

    exibir("✅ Receita adicionada!")
    limpar_campos()

def adicionar_despesa():
    try:
        valor = float(entry_valor.get().replace(",", "."))
    except ValueError:
        exibir("⚠️ Valor inválido! Digite um número.")
        return

    carteira.adicionar_transacao(Despesa(
        entry_descricao.get(),
        valor,
        entry_data.get(),
        entry_categoria.get()
    ))

    exibir("✅ Despesa adicionada!")
    limpar_campos()


tk.Button(frame_form, text="✅ Adicionar Receita", command=adicionar_receita).grid(row=4, column=0, pady=10)
tk.Button(frame_form, text="❌ Adicionar Despesa", command=adicionar_despesa).grid(row=4, column=1, pady=10)

if __name__ == "__main__":
    janela.mainloop()
