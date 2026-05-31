import sqlite3


def conexao():
    conn = sqlite3.connect('gastos.db')
    return conn
    
    
def criar_tabela():
    conn = conexao()
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descricao TEXT,
    valor REAL,
    categoria TEXT,
    data TEXT
)        
''')
    
    conn.commit()
    conn.close()