from models.transacao import Transacao, TipoTransacao
from database.repositorio import salvar_transacao, listar_transacoes, deletar_transacao,buscar_por_categoria, resumo_por_categoria,editar_transacao,buscar_por_mes
import csv
class Carteira():
    
    def adicionar_transacao(self, transacao):
        salvar_transacao(transacao)
        
    
    def deletar(self, id):
        deletar_transacao(id)
        
        print(f"🗑️ Transação {id} deletada com sucesso!")    
    
    def calcular_saldo(self):
        listar = listar_transacoes()
        saldo = 0
        for t in listar:
            if t[1] == "receita":
                saldo += t[3]

            else:
                saldo -= t[3]
        print(f"💰 Saldo atual: R$ {saldo}")
            
    def listar(self):
        transacoes = listar_transacoes()
        
        for t in transacoes:
            emoji = "✅" if t[1] == "receita" else "❌"
            print(f"ID: {t[0]} | {emoji} {t[1]} | {t[2]} | R$ {t[3]} | {t[4]} | {t[5]}")
            
    def filtrar_categoria(self, categoria):
        transacoes = buscar_por_categoria(categoria)
        
        if not transacoes:
            print(f"⚠️ Nenhuma transação encontrada para a categoria: {categoria}")
            return
        
        for filtro in transacoes:
            
            emoji = "✅" if filtro[1] == "receita" else "⚠️"
            print(f"ID: {filtro[0]} | {emoji} {filtro[1]} | {filtro[2]} | R$ {filtro[3]} | {filtro[4]} | {filtro[5]}")
                
    def resumo(self):
        resumo = resumo_por_categoria()
        
        if not resumo:
            print("⚠️ Nenhuma despesa registrada.") 
            return
        
        for r in resumo:
           print("📊 Resumo de gastos por categoria:")
           print(f"🔸 {r[0]}: R$ {r[1]}")
    
    def editar(self, id, descricao, valor, data, categoria):
        editar_transacao(id, descricao, valor, data, categoria)
        
        print(f"✏️ Transação {id} editada com sucesso!")
        
        
    def filtrar_mes(self, mes):
        lista_mes = buscar_por_mes(mes)
        
        if not lista_mes:
            print(f"⚠️ Nenhuma transação encontrada para o mês: {mes}")
            return
        
        for mes in lista_mes:
            emoji = "✅" if mes[1] == "receita" else "❌"
            print(f"ID: {mes[0]} | {emoji} {mes[1]} | {mes[2]} | R$ {mes[3]} | {mes[4]} | {mes[5]}")
    
    def exportar_csv(self):
        listar_transacoes()
        
   
    def exportar_csv(self):
        transacoes = listar_transacoes()
        
        with open("relatorio.csv", "w", newline="", encoding="utf-8") as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow(["id", "tipo", "descricao", "valor", "categoria", "data"])
            
            for t in transacoes:
                writer.writerow(t)