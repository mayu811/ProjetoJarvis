from src.backend.db.database import get_connection

# ── Tarefas ───────────────────────────────────────────────────────────────────

def adicionar_tarefa(titulo: str, descricao: str = None, prazo: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tarefas (titulo, descricao, prazo) VALUES (?, ?, ?)",
        (titulo, descricao, prazo)
    )
    conn.commit()
    id_criado = cursor.lastrowid
    conn.close()
    return {"id": id_criado, "titulo": titulo, "descricao": descricao, "prazo": prazo}

def listar_tarefas(apenas_pendentes: bool = True) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    if apenas_pendentes:
        cursor.execute("SELECT * FROM tarefas WHERE concluida = 0 ORDER BY prazo")
    else:
        cursor.execute("SELECT * FROM tarefas ORDER BY prazo")
    tarefas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return tarefas

def concluir_tarefa(id_tarefa: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET concluida = 1 WHERE id = ?", (id_tarefa,))
    conn.commit()
    alteradas = cursor.rowcount
    conn.close()
    return {"sucesso": alteradas > 0, "id": id_tarefa}

# ── Compromissos ──────────────────────────────────────────────────────────────

def adicionar_compromisso(titulo: str, data_hora: str, descricao: str = None, local: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO compromissos (titulo, descricao, data_hora, local) VALUES (?, ?, ?, ?)",
        (titulo, descricao, data_hora, local)
    )
    conn.commit()
    id_criado = cursor.lastrowid
    conn.close()
    return {"id": id_criado, "titulo": titulo, "data_hora": data_hora}

def consultar_agenda(data: str = None) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    if data:
        cursor.execute(
            "SELECT * FROM compromissos WHERE data_hora LIKE ? ORDER BY data_hora",
            (f"{data}%",)
        )
    else:
        cursor.execute("SELECT * FROM compromissos ORDER BY data_hora")
    compromissos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return compromissos