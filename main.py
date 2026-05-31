from models.transacao import Transacao

teste = Transacao(banco='Nubank', descricao='teste',valor=20, data='31/05/2026', categoria='cartão virtual' )

print(teste)