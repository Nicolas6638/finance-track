from database.conexao import get_conexao

def criar_orcamento(orcamento):
    with get_conexao() as conn:
        conn.execute("INSERT INTO orcamentos(categoria, mes, limite) VALUES(?, ?, ?)", (orcamento.categoria, orcamento.mes, orcamento.limite))
    
def listar_orcamentos():
    with get_conexao() as conn:
        return conn.execute("SELECT * FROM orcamentos ORDER BY mes DESC").fetchall()

def buscar_por_categoria_e_mes(categoria, mes):
    with get_conexao() as conn:
        return conn.execute("SELECT * FROM orcamentos WHERE categoria = ? AND mes = ?", (categoria, mes)).fetchall()
    
    
def deletar_orcamento(id):
    with get_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM orcamentos WHERE id = ?", (id,))
        conn.commit()
        return cursor.rowcount > 0

def atualizar_orcamento(id, limite):
    with get_conexao() as conn:
        conn.execute("UPDATE orcamentos SET limite = ? WHERE id = ?", (limite, id))
        conn.commit()