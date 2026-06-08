from models.transacao import Transacao, TipoTransacao
from database.repositorio import (salvar_transacao, listar_transacoes, deletar_transacao,buscar_por_categoria, resumo_por_categoria,editar_transacao,buscar_por_mes)
import csv

class Carteira():
    
    def adicionar_transacao(self, transacao):
        salvar_transacao(transacao)
        
    
    def deletar(self, id_transacao: int):
        deletar_transacao(id_transacao)
           
    
    def calcular_saldo(self) -> float:
        transacao = listar_transacoes()
        saldo = 0.0
        for t in transacao:
            _, tipo, _, valor, _, _ = t 
            saldo += valor if tipo == "receita" else - valor

        return saldo
            
    def listar(self) -> list:
        return listar_transacoes()
        
    def filtrar_categoria(self, categoria: str) -> list:
        return buscar_por_categoria(categoria)
             
    def resumo(self) -> list:
        return resumo_por_categoria()
        
    def editar(self, id_transacao: int, descricao: str, valor: float, data: str, categoria: str):
        editar_transacao(id_transacao, descricao, valor, data, categoria)
           
    def filtrar_mes(self, mes: str) -> list:
        return buscar_por_mes(mes)
        
   
    def exportar_csv(self, caminho= "relatorios.csv"):
        
        with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["id", "tipo", "descricao", "valor", "categoria", "data"])
            
            writer.writerow(self.listar())