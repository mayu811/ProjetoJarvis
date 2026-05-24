'''
    Aqui estabelecemos conexão com o banco de dados SQLite,
    além de inicializar suas tabelas, SE ainda ainda não existirem.

'''

import sqlite3
from pathlib import Path

DB_PATH = Path("src/backend/db/jarvis.db")

# 
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # retorna dicts em vez de tuplas
    # retorna variavel de conexão para ser usada nas funções de queries
    return conn

def inicializar_banco():
    conn = get_connection()
    # cursor para executar comandos SQL
    cursor = conn.cursor()

    #criação de tabelas de tarefas e compromissos (agenda), respectivamente abaixo:
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
            data_hora   TEXT NOT NULL,
            local       TEXT,
            criado_em   TEXT DEFAULT (datetime('now'))
        );
    """)
    
    conn.commit()
    conn.close()
    print("Banco inicializado.")