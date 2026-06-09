import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import conexao
from models.transacao import Transacao, TipoTransacao
from models.carteira import Carteira


class TestTransacao(unittest.TestCase):
    def test_criar_receita_valida(self):
        t = Transacao(TipoTransacao.RECEITA, "Salário", 3500.0, "01/06/2026", "Renda")
        self.assertIs(t.tipo, TipoTransacao.RECEITA)
        self.assertEqual(t.valor, 3500.0)

    def test_criar_despesa_valida(self):
        t = Transacao(TipoTransacao.DESPESA, "Aluguel", 1200.0, "05/06/2026", "Moradia")
        self.assertIs(t.tipo, TipoTransacao.DESPESA)

    def test_valor_zero_raise(self):
        with self.assertRaises(ValueError):
            Transacao(TipoTransacao.RECEITA, "teste", 0, "01/06/2026", "cat")

    def test_valor_negativo_raise(self):
        with self.assertRaises(ValueError):
            Transacao(TipoTransacao.RECEITA, "teste", -10, "01/06/2026", "cat")

    def test_data_invalida_raise(self):
        with self.assertRaises(ValueError):
            Transacao(TipoTransacao.RECEITA, "teste", 10, "32/13/AAAA", "cat")

    def test_data_formato_invalido_raise(self):
        with self.assertRaises(ValueError):
            Transacao(TipoTransacao.RECEITA, "teste", 10, "2026-06-01", "cat")

    def test_descricao_vazia_raise(self):
        with self.assertRaises(ValueError):
            Transacao(TipoTransacao.RECEITA, "", 10, "01/06/2026", "cat")

    def test_descricao_so_espacos_raise(self):
        with self.assertRaises(ValueError):
            Transacao(TipoTransacao.RECEITA, "   ", 10, "01/06/2026", "cat")

    def test_categoria_vazia_raise(self):
        with self.assertRaises(ValueError):
            Transacao(TipoTransacao.RECEITA, "teste", 10, "01/06/2026", "")

    def test_str_receita(self):
        t = Transacao(TipoTransacao.RECEITA, "Salário", 3500, "01/06/2026", "Renda")
        self.assertIn("✅", str(t))

    def test_str_despesa(self):
        t = Transacao(TipoTransacao.DESPESA, "Conta", 100, "01/06/2026", "Casa")
        self.assertIn("❌", str(t))


class TestCarteira(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_fd, cls.db_path = tempfile.mkstemp(suffix=".db")
        conexao.DB_PATH = cls.db_path

    @classmethod
    def tearDownClass(cls):
        os.close(cls.db_fd)
        os.unlink(cls.db_path)

    def setUp(self):
        conexao.criar_tabela()
        self.carteira = Carteira()

    def tearDown(self):
        import sqlite3
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM transacoes")

    def test_listar_vazia(self):
        self.assertEqual(self.carteira.listar(), [])

    def test_adicionar_e_listar(self):
        t = Transacao(TipoTransacao.RECEITA, "Salário", 3500, "01/06/2026", "Renda")
        self.carteira.adicionar_transacao(t)
        transacoes = self.carteira.listar()
        self.assertEqual(len(transacoes), 1)
        self.assertEqual(transacoes[0][2], "Salário")

    def test_calcular_saldo_receita(self):
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.RECEITA, "Salário", 1000, "01/06/2026", "Renda"))
        self.assertEqual(self.carteira.calcular_saldo(), 1000.0)

    def test_calcular_saldo_receita_despesa(self):
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.RECEITA, "Salário", 2000, "01/06/2026", "Renda"))
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Conta", 500, "02/06/2026", "Casa"))
        self.assertEqual(self.carteira.calcular_saldo(), 1500.0)

    def test_calcular_saldo_vazio(self):
        self.assertEqual(self.carteira.calcular_saldo(), 0.0)

    def test_deletar_transacao_existente(self):
        t = Transacao(TipoTransacao.DESPESA, "Teste", 50, "01/06/2026", "cat")
        self.carteira.adicionar_transacao(t)
        id_ = self.carteira.listar()[-1][0]
        self.assertTrue(self.carteira.deletar(id_))
        self.assertEqual(len(self.carteira.listar()), 0)

    def test_deletar_transacao_inexistente(self):
        self.assertFalse(self.carteira.deletar(9999))

    def test_filtrar_categoria(self):
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Uber", 20, "01/06/2026", "Transporte"))
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Gasolina", 100, "02/06/2026", "Transporte"))
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.RECEITA, "Freela", 500, "03/06/2026", "Trabalho"))
        transacoes = self.carteira.filtrar_categoria("Transporte")
        self.assertEqual(len(transacoes), 2)

    def test_filtrar_categoria_sem_resultado(self):
        self.assertEqual(self.carteira.filtrar_categoria("inexistente"), [])

    def test_resumo_por_categoria(self):
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Uber", 20, "01/06/2026", "Transporte"))
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Gasolina", 100, "02/06/2026", "Transporte"))
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Aluguel", 800, "01/06/2026", "Moradia"))
        resumo = self.carteira.resumo()
        self.assertEqual(len(resumo), 2)
        total_transporte = next(r[1] for r in resumo if r[0] == "Transporte")
        self.assertEqual(total_transporte, 120.0)

    def test_resumo_sem_despesas(self):
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.RECEITA, "Salário", 5000, "01/06/2026", "Renda"))
        self.assertEqual(self.carteira.resumo(), [])

    def test_filtrar_mes(self):
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Conta", 100, "05/06/2026", "Casa"))
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.RECEITA, "Salário", 3000, "01/07/2026", "Renda"))
        transacoes = self.carteira.filtrar_mes("06/2026")
        self.assertEqual(len(transacoes), 1)

    def test_filtrar_mes_sem_resultado(self):
        self.assertEqual(self.carteira.filtrar_mes("01/2025"), [])

    def test_editar_transacao(self):
        t = Transacao(TipoTransacao.DESPESA, "Antigo", 100, "01/06/2026", "cat")
        self.carteira.adicionar_transacao(t)
        id_ = self.carteira.listar()[-1][0]
        self.carteira.editar(id_, "receita", "Novo", 200, "02/06/2026", "nova_cat")
        editada = self.carteira.listar()[-1]
        self.assertEqual(editada[1], "receita")
        self.assertEqual(editada[2], "Novo")
        self.assertEqual(editada[3], 200.0)

    def test_listar_ordem_decrescente_data(self):
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Primeiro", 10, "01/01/2026", "cat"))
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.DESPESA, "Segundo", 20, "02/01/2026", "cat"))
        transacoes = self.carteira.listar()
        self.assertEqual(transacoes[0][2], "Segundo")
        self.assertEqual(transacoes[1][2], "Primeiro")

    def test_exportar_csv(self):
        self.carteira.adicionar_transacao(
            Transacao(TipoTransacao.RECEITA, "Teste", 100, "01/06/2026", "cat"))
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            caminho = f.name
        try:
            self.carteira.exportar_csv(caminho)
            with open(caminho, encoding="utf-8") as f:
                conteudo = f.read()
            self.assertIn("id,tipo,descricao,valor,categoria,data", conteudo)
            self.assertIn("Teste", conteudo)
        finally:
            os.unlink(caminho)


if __name__ == "__main__":
    unittest.main()