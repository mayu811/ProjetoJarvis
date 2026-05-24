'''
    Aqui estabelecemos conexão com o banco de dados SQLite,
    além de inicializar suas tabelas, SE ainda não existirem.
'''
import sqlite3
from pathlib import Path

DB_PATH = Path("src/backend/db/jarvis.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # retorna dicts em vez de tuplas
    return conn

def inicializar_banco():
    conn = get_connection()
    cursor = conn.cursor()
    # criação das tabelas de tarefas e compromissos (agenda), respectivamente:
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo      TEXT NOT NULL,
            descricao   TEXT,
            prazo       TEXT,
            prioridade  TEXT DEFAULT 'baixa',
            concluida   INTEGER DEFAULT 0,
            criada_em   TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS compromissos (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo      TEXT NOT NULL,
            descricao   TEXT,
            data_hora   TEXT,
            local       TEXT,
            criado_em   TEXT DEFAULT (datetime('now'))
        );
    """)
    conn.commit()
    conn.close()
    print("[DB] Banco inicializado.")