from models.carteira import Carteira
from models.receita import Receita
from models.despesa import Despesa
import tkinter as tk
import sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

janela = tk.Tk()
janela.title("💰 Organizador Financeiro")
janela.geometry("600x400")

label = tk.Label(janela, text="💰 Organizador Financeiro", font=("Arial", 18, "bold"))
label.pack(pady=20)

carteira = Carteira()

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=20)

tk.Button(frame_botoes, text="📋 Listar Transações", width=25, 
          command=lambda: carteira.listar()).pack(pady=5)

tk.Button(frame_botoes, text="💰 Ver Saldo", width=25, 
          command=lambda: exibir(f"💰 Saldo atual: R$ {carteira.calcular_saldo()}")).pack(pady=5)

tk.Button(frame_botoes, text="📊 Resumo por Categoria", width=25, 
          command=lambda: carteira.resumo()).pack(pady=5)

tk.Button(frame_botoes, text="❌ Sair", width=25, 
          command=janela.destroy).pack(pady=5)

frame_form = tk.LabelFrame(janela, text="Nova Transção", padx=10, pady=10)
frame_form.pack(pady=10, padx=20, fill="x")

frame_resultado = tk.LabelFrame(janela, text="📋 Resultados", padx=10, pady=10)
frame_resultado.pack(pady=10, padx=20, fill="both", expand=True)

texto_resultado = tk.Text(frame_resultado, height=10, width=70)
texto_resultado.pack()

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

def adicionar_receita():
    carteira.adicionar_transacao(Receita(
        entry_descricao.get(),
        float(entry_valor.get()),
        entry_data.get(),
        entry_categoria.get()
    ))
    
    print("✅ Receita adicionada!")
    
def adicionar_despesa():
    carteira.adicionar_transacao(Despesa(
        entry_descricao.get(),
        float(entry_valor.get()),
        entry_data.get(),
        entry_categoria.get()
    ))
    
    print("✅ Despesa adicionada!")
    
def exibir(mensagem):
    texto_resultado.insert(tk.END, mensagem + "\n")
    texto_resultado.see(tk.END)
    


tk.Button(frame_form, text="✅ Adicionar Receita", command=adicionar_receita).grid(row=4, column=0, pady=10)
tk.Button(frame_form, text="❌ Adicionar Despesa", command=adicionar_despesa).grid(row=4, column=1, pady=10)

janela.mainloop()
