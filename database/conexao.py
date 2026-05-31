import sqlite3


def conexao(conn):
    conn = sqlite3.connect('gastos.db')
    
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes(
    id INTERGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descricao TEXT,
    valor REAL.
    categoria TEXT,
    data TEXT
)        
''')