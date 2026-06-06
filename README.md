# 💰 Organizador Financeiro

> Aplicação Python para controle financeiro pessoal — desenvolvida como projeto de portfólio.

![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python)
![SQLite](https://img.shields.io/badge/SQLite-003B57?logo=sqlite)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![Licença](https://img.shields.io/badge/licença-MIT-orange)

---

## ✨ Funcionalidades

- **Adicionar receitas e despesas** com descrição, valor, data e categoria
- **Listar** todas as transações cadastradas
- **Editar** e **deletar** transações
- **Filtrar** transações por categoria ou mês
- **Ver saldo** atual (receitas - despesas)
- **Resumo de gastos** agrupado por categoria
- **Exportar relatório** em CSV

---

## 🚀 Começando

Não há dependências externas — apenas Python puro com a biblioteca padrão.

### 📥 Instalação

```bash
# Clone o repositório
git clone https://github.com/Nicolas6638/finance-track.git

# Acesse a pasta
cd finance-track

# Pronto! É só executar.
```

### ▶️ Como usar

**Interface de Linha de Comando (CLI):**
```bash
python main.py
```

Menu interativo com 10 opções:

```
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
```

**Interface Gráfica (GUI):**
```bash
python tela.py
```

---

## 📁 Estrutura do Projeto

```
organizador-financeiro/
├── database/
│   ├── conexao.py          # 🔗 Conexão e criação da tabela SQLite
│   └── repositorio.py      # 🗃️ Funções CRUD do banco de dados
├── models/
│   ├── transacao.py        # 📄 Classe base Transacao
│   ├── receita.py          # 💵 Classe Receita
│   ├── despesa.py          # 💸 Classe Despesa
│   └── carteira.py         # 🧠 Lógica de negócio
├── test/
│   └── teste.py            # 🧪 Testes
├── main.py                 # 🖥️ Interface CLI
├── tela.py                 # 🖼️ Interface gráfica (Tkinter)
├── gastos.db               # 🗄️ Banco de dados SQLite
└── README.md
```

---

## 🏗️ Arquitetura

O projeto segue uma arquitetura em **3 camadas**:

```
┌──────────────────────────────────────┐
│         APRESENTAÇÃO                 │
│   main.py (CLI)  •  tela.py (GUI)   │
├──────────────────────────────────────┤
│            NEGÓCIO                   │
│   Carteira • Transacao • Receita    │
│   Despesa                            │
├──────────────────────────────────────┤
│             DADOS                    │
│   conexao.py • repositorio.py       │
│   └── SQLite (gastos.db)            │
└──────────────────────────────────────┘
```

---

## 🛠️ Tecnologias

| Tecnologia | Função |
|---|---|
| **Python 3.12+** | Linguagem principal |
| **SQLite3** | Banco de dados local |
| **Tkinter** | Interface gráfica |

> ⚡ Zero dependências externas — tudo o que você precisa já vem com o Python.

---

## 📊 Exemplo de Uso (CLI)

```text
💰 Organizador Financeiro
==========================
1. Adicionar Receita
> Descrição: Salário
> Valor: 3500
> Data (DD/MM/AAAA): 05/06/2026
> Categoria: Renda
✅ Receita adicionada!

> Saldo atual: R$ 3.500,00
```

---

## 👨‍💻 Autor

**Nicolas Dev** — [nicolasmanuel108@gmail.com](mailto:nicolasmanuel108@gmail.com)

Projeto desenvolvido como parte do portfólio pessoal.

---

## 📄 Licença

Este projeto está sob a licença MIT.
