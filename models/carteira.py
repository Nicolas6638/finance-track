from models.receita import Receita
from models.despesa import Despesa
from database.repositorio import salvar_transacao, listar_transacoes

class Carteira():
    
    def adicionar_transacao(self, transacao):
        salvar_transacao(transacao)
            
    
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