from database.conexao import get_conexao

def salvar_transacao(transacao):
    with get_conexao() as conn:
        conn.execute("INSERT INTO transacoes (tipo, descricao, valor, categoria, data) VALUES (?, ?, ?, ?, ?)",
                     (transacao.tipo.value, transacao.descricao, transacao.valor,
                      transacao.categoria, transacao.data))
            
def listar_transacoes():
    with get_conexao() as conn: 
        cursor = conn.cursor()
        return cursor.execute("SELECT * FROM transacoes ORDER BY data DESC").fetchall()


def deletar_transacao(id):
    with get_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0
   

def buscar_por_categoria(categoria):
    with get_conexao() as conn:
        cursor = conn.cursor()
        return  cursor.execute("SELECT * FROM transacoes WHERE categoria = ?", (categoria,)).fetchall()
   
def resumo_por_categoria():
    with get_conexao() as conn:
        cursor = conn.cursor()
        return cursor.execute("""
        SELECT categoria, SUM(valor) FROM transacoes
        WHERE tipo = 'despesa'
        GROUP BY categoria
                   """).fetchall()

def editar_transacao(id, tipo, descricao, valor, data, categoria):
    with get_conexao() as conn:
        conn.execute("""
        UPDATE transacoes
        SET tipo = ?, descricao = ?, valor = ?, data = ?, categoria = ?
        WHERE id = ?
        """, (tipo, descricao, valor, data, categoria, id))
  
    
def buscar_por_mes(mes):
    with get_conexao() as conn:
        cursor = conn.cursor()
    
        return cursor.execute("""
        SELECT * FROM transacoes 
        WHERE substr(data, 4, 7) = ?          
                   """, (mes,)).fetchall()

