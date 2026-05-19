from src.backend.db.database import get_connection

def adicionar_tarefa(titulo: str, prazo: str = None, prioridade: str = "baixa") -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tarefas (titulo, prazo, prioridade) VALUES (?, ?, ?)",
        (titulo, prazo, prioridade)
    )
    conn.commit()
    conn.close()
    return {"ok": True, "mensagem": f"Tarefa '{titulo}' adicionada com sucesso."}

def listar_tarefas() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tarefas WHERE concluida = 0 ORDER BY prazo")
    tarefas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    if not tarefas:
        return {"ok": True, "mensagem": "Nenhuma tarefa pendente."}
    return {"ok": True, "tarefas": tarefas}

def concluir_tarefa(titulo: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tarefas SET concluida = 1 WHERE LOWER(titulo) = LOWER(?)", (titulo,))
    conn.commit()
    alteradas = cursor.rowcount
    conn.close()
    if alteradas == 0:
        return {"ok": False, "mensagem": f"Tarefa '{titulo}' não encontrada."}
    return {"ok": True, "mensagem": f"Tarefa '{titulo}' concluída."}

def adicionar_compromisso(titulo: str, data_hora: str, descricao: str = None, local: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO compromissos (titulo, descricao, data_hora, local) VALUES (?, ?, ?, ?)",
        (titulo, descricao, data_hora, local)
    )
    conn.commit()
    conn.close()
    return {"ok": True, "mensagem": f"Compromisso '{titulo}' adicionado com sucesso."}

def consultar_agenda(data: str = None) -> dict:
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
    if not compromissos:
        return {"ok": True, "mensagem": "Nenhum compromisso na agenda."}
    return {"ok": True, "compromissos": compromissos}