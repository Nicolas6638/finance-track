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

def buscar_por_categoria(categoria):
    conn = conexao()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM transacoes WHERE categoria = ?", (categoria,))
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def resumo_por_categoria():
    conn = conexao()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT categoria, SUM(valor) FROM transacoes
        WHERE tipo = 'despesa'
        GROUP BY categoria
                   """)
    resultado = cursor.fetchall()
    conn.close()
    return resultado

def editar_transacao(id, descricao, valor, data, categoria):
    conn = conexao()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE transacoes
        SET descricao = ?, valor = ?, data = ?, categoria =?
        WHERE id = ?   
                   """, (descricao, valor, data, categoria, id))
    
    conn.commit()
    conn.close()
    
def buscar_por_mes(mes):
    conn = conexao()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM transacoes 
        WHERE data LIKE ?          
                   """, (f"%{mes}",))    
    
    resultado = cursor.fetchall()
    conn.close()
    return resultado

