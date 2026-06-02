from database.conexao import conexao

def salvar_transacao(transacao):
    conn = conexao()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO transacoes (tipo, descricao, valor, categoria, data) VALUES (?, ?, ?, ?, ?)", (transacao.tipo, transacao.descricao, transacao.valor,transacao.categoria, transacao.data))
    
    conn.commit()
    conn.close()
    
def listar_transacoes():
    conn = conexao()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transacoes")
    resultado = cursor.fetchall()
    
    conn.close()
    return resultado

def deletar_transacao(id):
    conn = conexao()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
    conn.commit()
    conn.close()

