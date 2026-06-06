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
    tipo TEXT,
    descricao TEXT,
    valor REAL,
    categoria TEXT,
    data TEXT
)        
''')
    
        conn.commit()
