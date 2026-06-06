import sqlite3

DB_PATH = 'gastos.db'

def get_conexao():
    return sqlite3.connect(DB_PATH)
        
    
def criar_tabela():
    with get_conexao() as conn:
        cursor = conn.cursor()
    
        cursor.execute('''
    CREATE TABLE IF NOT EXISTS transacoes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL,
    categoria TEXT NOT NULL,
    data TEXT NOT NULL
)        
''')
    
        conn.commit()
