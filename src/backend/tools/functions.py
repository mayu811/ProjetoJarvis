'''
    Aqui estão as funções queries que interagem diretamente com o banco de dados SQLite, 
    usando a função get_connection() definida em database.py para obter uma conexão com o banco.

'''

# ------------ IMPORTAÇÕES --------------#

# funções para interagir com o banco de dados (SQLite)
from src.backend.db.database import get_connection


#importação do módulo de indexação para verificar se os índices estão prontos antes de tentar recuperar material
import src.backend.rag.indexer as indexer  # importa o módulo, não a variável

#importação do módulo de geração para usar a função de resposta RAG dentro da função buscar_material_rag
from src.backend.rag.generator import responder_rag

#importação do cliente para usar a função de resposta RAG dentro da função planejar_estudos
from src.backend.rag.indexer import indice_faiss
from src.backend.rag.generator import responder_rag
from src.backend.rag.connection import client
import json


# ---------------------- TAREFAS ---------------------- #

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
    # seleciona apenas as tarefas que não foram concluídas, ordenando pela data de prazo
    cursor.execute("SELECT * FROM tarefas WHERE concluida = 0 ORDER BY prazo")
    tarefas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    # se não houver tarefas pendentes, retorna uma mensagem indicando
    if not tarefas:
        return {"ok": True, "mensagem": "Nenhuma tarefa pendente."}
    # caso contrário, retorna a lista de tarefas
    return {"ok": True, "tarefas": tarefas}


def listar_tarefas_concluidas() -> dict:

    conn = get_connection()
    cursor = conn.cursor()
    # seleciona apenas as tarefas que foram concluídas, ordenando pela data de prazo
    cursor.execute("SELECT * FROM tarefas WHERE concluida = 1 ORDER BY prazo DESC")
    tarefas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    # se não houver tarefas concluídas, retorna uma mensagem indicando
    if not tarefas:
        return {"ok": True, "mensagem": "Nenhuma tarefa concluída."}
    # caso contrário, retorna a lista de tarefas
    return {"ok": True, "tarefas": tarefas}


def concluir_tarefa(titulo: str) -> dict:
    '''
        Marca a tarefa com o título especificado como concluída. 
        A comparação do título é feita de forma case-insensitive para facilitar a identificação da tarefa, 
        mesmo que o usuário não tenha digitado exatamente igual. Se nenhuma tarefa for encontrada com 
        o título fornecido, retorna uma mensagem indicando que a tarefa não foi encontrada.
    '''

    conn = get_connection()
    cursor = conn.cursor()
    # marca a tarefa como concluída, comparando o título de forma case-insensitive
    cursor.execute("UPDATE tarefas SET concluida = 1 WHERE LOWER(titulo) = LOWER(?)", (titulo,))
    conn.commit()

    alteradas = cursor.rowcount # número de linhas alteradas, para verificar se a tarefa foi encontrada
    conn.close()

    # se nenhuma linha foi alterada, significa que a tarefa não foi encontrada
    if alteradas == 0:
        return {"ok": False, "mensagem": f"Tarefa '{titulo}' não encontrada."}
    return {"ok": True, "mensagem": f"Tarefa '{titulo}' concluída."}



# ---------------------- COMPROMISSOS (AGENDA) ---------------------- #

def adicionar_compromisso(titulo: str, data_hora: str, descricao: str = None, local: str = None) -> dict:

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        # insere um novo compromisso na tabela de compromissos, com os dados fornecidos
        "INSERT INTO compromissos (titulo, descricao, data_hora, local) VALUES (?, ?, ?, ?)",
        (titulo, descricao, data_hora, local)
    )
    conn.commit()
    conn.close()
    return {"ok": True, "mensagem": f"Compromisso '{titulo}' adicionado com sucesso."}


def remover_compromisso(titulo: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    # remove o compromisso com o título especificado, comparando de forma case-insensitive
    cursor.execute("DELETE FROM compromissos WHERE LOWER(titulo) = LOWER(?)", (titulo,))
    conn.commit()
    alterados = cursor.rowcount # número de linhas alteradas, para verificar se o compromisso foi encontrado
    conn.close()
    # se nenhuma linha foi alterada, significa que o compromisso não foi encontrado
    if alterados == 0:
        return {"ok": False, "mensagem": f"Compromisso '{titulo}' não encontrado."}
    return {"ok": True, "mensagem": f"Compromisso '{titulo}' removido."}


def consultar_agenda(data: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    # se uma data específica for fornecida, seleciona apenas os compromissos dessa data
    # caso contrário, seleciona todos os compromissos futuros, ordenando pela data e hora
    if data:
        cursor.execute(
            "SELECT * FROM compromissos WHERE data_hora LIKE ? ORDER BY data_hora",
            (f"{data}%",)
        )
    else:
        cursor.execute("SELECT * FROM compromissos ORDER BY data_hora")
    # converte os resultados para uma lista de dicionários, onde cada dicionário representa um compromisso
    compromissos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    # se não houver compromissos, retorna uma mensagem indicando que a agenda está vazia
    if not compromissos:
        return {"ok": True, "mensagem": "Nenhum compromisso na agenda."}
    return {"ok": True, "compromissos": compromissos}


# ---------------------- FUNÇÕES RAGS ----------------------

def buscar_material_rag(pergunta: str) -> dict:

    if indexer.indice_faiss is None or indexer.indice_bm25 is None:
        return {"ok": False, "mensagem": "Nenhum documento foi enviado ainda. Envie um arquivo primeiro."}

    resposta, docs = responder_rag(pergunta, k=10)

    print(f"\n=== BUSCAR_MATERIAL_RAG ===")
    print(f"Resposta do generator: {resposta[:200]}")
    print(f"Docs: {len(docs)}")
    print("===\n")

    if not docs:
        return {"ok": False, "mensagem": "Nenhum material encontrado nos documentos."}

    return {"ok": True, "contexto": resposta}


def planejar_estudos(pergunta: str) -> dict:

    tarefas = listar_tarefas()
    agenda = consultar_agenda()

    contexto_rag = None
    if indice_faiss is not None:
        resposta_rag, docs = responder_rag(pergunta, k=10)
        if docs:
            contexto_rag = resposta_rag

    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        #monta o prompt incluindo a pergunta, as tarefas pendentes, a agenda e o contexto RAG (se disponível)
        messages=[
            {
                "role": "system",
                "content": """Você é um assistente acadêmico especializado em planejamento de estudos.
                Com base nas tarefas pendentes, agenda e materiais fornecidos, monte um plano de estudos claro e objetivo.
                Use markdown para formatar. Seja específico e prático."""
            },
            
            {
                "role": "user",
                "content": f"""
                Solicitação: {pergunta}

                Tarefas pendentes:
                {json.dumps(tarefas, ensure_ascii=False)}

                Agenda:
                {json.dumps(agenda, ensure_ascii=False)}

                Conteúdo dos documentos relevantes:
                {contexto_rag or "Nenhum documento enviado."}
                """
            }
        ]
    )

    return {"ok": True, "contexto": resp.choices[0].message.content}
