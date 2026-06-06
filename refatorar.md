# Guia de Refatoração — Organizador Financeiro

## Problemas Gerais do Projeto

| Problema | Onde | Impacto |
|---|---|---|
| Camada de negócio usa `print()` em vez de retornar dados | `models/carteira.py` | GUI precisa de `capturar_print()` gambiarra |
| Conexão com banco aberta/fechada manualmente toda função | `database/` | Código repetido, risco de leak |
| Herança desnecessária em `Receita`/`Despesa` | `models/` | Só diferem no `tipo` — uma classe + enum resolve |
| Duplicação de código (ex: `exportar_csv` definido 2x) | `models/carteira.py:74-86` | Método morto sobrescrito |
| Importações não utilizadas | `main.py:4-5` | Ruído, confunde |
| Nenhuma validação de entrada | `main.py`, `tela.py` | Crash com input inválido |
| Teste não testa nada | `test/teste.py` | Apenas lista, sem assertions |
| `criar_tabela()` nunca chamada | `database/conexao.py` | Tabela pode não existir |
| Bug: `case 4` chama `deletar()` duas vezes | `main.py:57-59` | Crash na primeira chamada sem args |
| Bug: `case 2` printa "Receita" no lugar de "Despesa" | `main.py:51` | Mensagem errada |
| Typo "Transção" em vez de "Transação" | `main.py:75` | Erro de digitação |

---

## 1. `database/conexao.py` — Conexão com SQLite

**Problemas:**
- Toda função abre e fecha conexão manualmente → duplicação de código
- `gastos.db` fixo no código — sem flexibilidade
- `criar_tabela()` nunca é chamada na aplicação

**Refatoração:**

```python
import sqlite3

DB_PATH = "gastos.db"

def get_conexao():
    return sqlite3.connect(DB_PATH)

def criar_tabela():
    with get_conexao() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tipo TEXT NOT NULL,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                categoria TEXT NOT NULL,
                data TEXT NOT NULL
            )
        """)
        conn.commit()
```

**O que aprender:** `with conn:` gerencia commit/rollback automaticamente. Constantes em maiúsculo. NOT NULL no schema garante integridade.

---

## 2. `database/repositorio.py` — CRUD

**Problemas:**
- Cada função abre/fecha conexão individualmente
- `editar_transacao` não permite editar tipo (receita/despesa)
- `buscar_por_mes` usa LIKE com formato frágil

**Refatoração:**

```python
from database.conexao import get_conexao

def salvar_transacao(transacao):
    with get_conexao() as conn:
        conn.execute(
            "INSERT INTO transacoes (tipo, descricao, valor, categoria, data) VALUES (?, ?, ?, ?, ?)",
            (transacao.tipo, transacao.descricao, transacao.valor, transacao.categoria, transacao.data)
        )

def listar_transacoes():
    with get_conexao() as conn:
        return conn.execute("SELECT * FROM transacoes ORDER BY data DESC").fetchall()

def deletar_transacao(id):
    with get_conexao() as conn:
        conn.execute("DELETE FROM transacoes WHERE id = ?", (id,))

def buscar_por_categoria(categoria):
    with get_conexao() as conn:
        return conn.execute(
            "SELECT * FROM transacoes WHERE categoria = ?", (categoria,)
        ).fetchall()

def resumo_por_categoria():
    with get_conexao() as conn:
        return conn.execute("""
            SELECT categoria, SUM(valor) FROM transacoes
            WHERE tipo = 'despesa'
            GROUP BY categoria
        """).fetchall()

def editar_transacao(id, tipo, descricao, valor, data, categoria):
    with get_conexao() as conn:
        conn.execute("""
            UPDATE transacoes
            SET tipo = ?, descricao = ?, valor = ?, data = ?, categoria = ?
            WHERE id = ?
        """, (tipo, descricao, valor, data, categoria, id))

def buscar_por_mes(mes):
    with get_conexao() as conn:
        return conn.execute(
            "SELECT * FROM transacoes WHERE substr(data, 4, 7) = ?", (mes,)
        ).fetchall()
```

**O que aprender:** `conn.execute()` direto (sem cursor) é suficiente. `ORDER BY` organiza a saída. `substr()` é mais seguro que `LIKE` para extrair mês.

---

## 3. `models/transacao.py` → Modelos (unificar herança)

**Problemas:**
- Herança desnecessária — `Receita` e `Despesa` só diferem no `tipo`
- `__str__` duplicado em cada classe
- Sem validação (valor negativo? data vazia?)

**Refatoração — eliminar herança:**

```python
# models/transacao.py
from enum import Enum

class TipoTransacao(Enum):
    RECEITA = "receita"
    DESPESA = "despesa"

class Transacao:
    def __init__(self, tipo: TipoTransacao, descricao: str, valor: float, data: str, categoria: str):
        if valor <= 0:
            raise ValueError("Valor deve ser positivo")
        self.tipo = tipo
        self.descricao = descricao
        self.valor = valor
        self.data = data
        self.categoria = categoria

    def __str__(self):
        emoji = "✅" if self.tipo == TipoTransacao.RECEITA else "❌"
        return f"{emoji} {self.descricao} | R$ {self.valor:.2f} | {self.categoria} | {self.data}"
```

Depois remova `receita.py` e `despesa.py` — o uso fica:

```python
from models.transacao import Transacao, TipoTransacao

# Uso:
Transacao(TipoTransacao.RECEITA, "Salário", 3500, "05/06/2026", "Renda")
```

**O que aprender:** `Enum` para valores fixos. Type hints melhoram legibilidade. Menos classes = menos manutenção.

---

## 4. `models/carteira.py` — Lógica de Negócio (principal problema)

**Problemas:**
| # | Problema | Detalhe |
|---|---|---|
| 1 | Importa `Receita` e `Despesa` mas nunca usa | Linhas 1-2 |
| 2 | `deletar()` — `main.py` chama sem args antes de chamar com args | Crash |
| 3 | Todos os métodos usam `print()` em vez de **retornar** dados | Impossível reuso na GUI |
| 4 | `resumo()` imprime cabeçalho dentro do loop | Repete a cada categoria |
| 5 | `exportar_csv()` **duplicado** — stub morto sobrescrito | Linhas 74-86 |
| 6 | `calcular_saldo()` acessa tuplas por índice numérico (`t[1]`, `t[3]`) | Frágil se schema mudar |
| 7 | Mistura responsabilidades: formatação visual + lógica + dados |

**Refatoração — métodos devem RETORNAR, não printar:**

```python
from database.repositorio import (
    salvar_transacao, listar_transacoes, deletar_transacao,
    buscar_por_categoria, resumo_por_categoria, editar_transacao, buscar_por_mes
)
import csv

class Carteira:
    def adicionar_transacao(self, transacao):
        salvar_transacao(transacao)

    def deletar(self, id_transacao: int):
        deletar_transacao(id_transacao)

    def calcular_saldo(self) -> float:
        transacoes = listar_transacoes()
        saldo = 0.0
        for t in transacoes:
            _, tipo, _, valor, _, _ = t
            saldo += valor if tipo == "receita" else -valor
        return saldo

    def listar(self) -> list:
        return listar_transacoes()

    def filtrar_categoria(self, categoria: str) -> list:
        return buscar_por_categoria(categoria)

    def resumo(self) -> list:
        return resumo_por_categoria()

    def editar(self, id_transacao: int, tipo: str, descricao: str, valor: float, data: str, categoria: str):
        editar_transacao(id_transacao, tipo, descricao, valor, data, categoria)

    def filtrar_mes(self, mes: str) -> list:
        return buscar_por_mes(mes)

    def exportar_csv(self, caminho="relatorio.csv"):
        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["id", "tipo", "descricao", "valor", "categoria", "data"])
            writer.writerows(self.listar())
```

**O que aprender:** Separação responsabilidades — negócio retorna dados, apresentação formata. Desempacotamento de tuplas (`_, tipo, _, valor, _, _ = t`).

---

## 5. `main.py` — CLI (Interface de Linha de Comando)

**Problemas:**
- `criar_tabela` importado mas nunca chamado
- Imports de `salvar_transacao`, `listar_transacoes`, `buscar_por_categoria` não usados
- `case 4`: chama `carteira.deletar()` sem argumento → crash
- `case 2` printa "✅ Receita adicionada!" em vez de "✅ Despesa adicionada!"
- `case 8`: "transção" em vez de "transação"
- Sem validação de entrada (`int()`, `float()` quebram com input inválido)
- Código do menu misturado com lógica

**Refatoração:**

```python
from database.conexao import criar_tabela
from models.carteira import Carteira
from models.transacao import Transacao, TipoTransacao

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
                    TipoTransacao.RECEITA,
                    input("Descrição: "),
                    ler_float("Valor: "),
                    input("Data (DD/MM/AAAA): "),
                    input("Categoria: ")
                )
                carteira.adicionar_transacao(t)
                print("✅ Receita adicionada!")

            case 2:
                t = Transacao(
                    TipoTransacao.DESPESA,
                    input("Descrição: "),
                    ler_float("Valor: "),
                    input("Data (DD/MM/AAAA): "),
                    input("Categoria: ")
                )
                carteira.adicionar_transacao(t)
                print("✅ Despesa adicionada!")

            case 3:
                opcao_listar()

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
                    print(f"⚠️ Nenhuma transação encontrada para {mes}")
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
```

**O que aprender:** Funções de validação reutilizáveis (`ler_float`, `ler_int`). `if __name__` permite import seguro. Separação do loop principal em `main()`.

---

## 6. `tela.py` — GUI (Interface Gráfica)

**Problemas:**
- `capturar_print()` é workaround porque `carteira` usava `print()` — some após refatoração
- Duplicação entre `adicionar_receita()` e `adicionar_despesa()`

**Refatoração — depois de arrumar `carteira.py`:**

```python
from models.carteira import Carteira
from models.transacao import Transacao, TipoTransacao
import tkinter as tk

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
```

**O que aprender:** Uma função genérica + `lambda` elimina duplicação. Sem `capturar_print()` — os métodos agora retornam dados.

---

## 7. `test/teste.py` — Testes

**Problemas:**
- Só lista transações — não testa nada
- Sem `unittest` ou `pytest`
- Não testa adicionar, editar, deletar, saldo

**Refatoração:**

```python
import unittest
import os
from models.transacao import Transacao, TipoTransacao
from models.carteira import Carteira
from database.conexao import criar_tabela, DB_PATH

class TestCarteira(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        criar_tabela()

    def setUp(self):
        self.carteira = Carteira()

    def test_adicionar_e_listar(self):
        t = Transacao(TipoTransacao.RECEITA, "Teste", 100, "01/01/2026", "teste")
        self.carteira.adicionar_transacao(t)
        transacoes = self.carteira.listar()
        self.assertGreater(len(transacoes), 0)

    def test_saldo_inicial(self):
        saldo = self.carteira.calcular_saldo()
        self.assertIsInstance(saldo, float)

    def test_deletar_transacao(self):
        t = Transacao(TipoTransacao.DESPESA, "Deletar", 50, "02/02/2026", "teste")
        self.carteira.adicionar_transacao(t)
        transacoes = self.carteira.listar()
        ultimo_id = transacoes[-1][0]
        self.carteira.deletar(ultimo_id)
        transacoes = self.carteira.listar()
        ids = [t[0] for t in transacoes]
        self.assertNotIn(ultimo_id, ids)

if __name__ == "__main__":
    unittest.main()
```

**O que aprender:** `setUpClass()` roda uma vez antes de todos os testes. `setUp()` roda antes de cada teste. Assertions validam comportamento.

---

## 8. Estrutura Final Sugerida

```
organizador-financeiro/
├── database/
│   ├── __init__.py
│   ├── conexao.py
│   └── repositorio.py
├── models/
│   ├── __init__.py
│   └── transacao.py        # Unifica Transacao + TipoTransacao enum
├── interface/
│   ├── __init__.py
│   ├── cli.py               # main.py renomeado e refatorado
│   └── gui.py               # tela.py renomeado e refatorado
├── tests/
│   ├── __init__.py
│   └── test_carteira.py
├── relatorio.csv
├── gastos.db
├── refatorar.md              # Este guia
├── README.md
└── requirements.txt          # (vazio — só stdlib)
```

---

## Checklist para Refatoração

- [ ] **conexao.py** — `with get_conexao()`, constantes, NOT NULL
- [ ] **repositorio.py** — remover cursor, `substr()` no filtro mês
- [ ] **transacao.py** — enum + classe única, remover `receita.py`/`despesa.py`
- [ ] **carteira.py** — métodos retornam dados, sem `print()`, desempacotar tuplas
- [ ] **main.py** → `cli.py` — validação, funções separadas, `if __name__`
- [ ] **tela.py** → `gui.py` — remover `capturar_print()`, lambda com enum
- [ ] **teste.py** → `tests/test_carteira.py` — unittest com assertions
- [ ] Rodar tudo e verificar se CLI e GUI funcionam
