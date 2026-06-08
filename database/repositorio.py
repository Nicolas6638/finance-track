from database.conexao import get_conexao

def salvar_transacao(transacao):
    with get_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO transacoes (tipo, descricao, valor, categoria, data) VALUES (?, ?, ?, ?, ?)", (transacao.tipo, transacao.descricao, transacao.valor,transacao.categoria, transacao.data))

        conn.commit()
            
def listar_transacoes():
    with get_conexao() as conn: 
        cursor = conn.cursor()
        return cursor.execute("SELECT * FROM transacoes ORDER BY data DESC").fetchall()


def deletar_transacao(id):
    with get_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
        
        conn.commit()
   

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

def editar_transacao(id, tipo,descricao, valor, data, categoria):
    with get_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE transacoes
        SET descricao = ?, valor = ?, data = ?, categoria =?
        WHERE id = ?   
                   """, (descricao, valor, data, categoria, id))
    
        conn.commit()
  
    
def buscar_por_mes(mes):
    with get_conexao() as conn:
        cursor = conn.cursor()
    
        return cursor.execute("""
        SELECT * FROM transacoes 
        WHERE substr(data, 4, 7) = ?          
                   """, (mes,)).fetchall()

