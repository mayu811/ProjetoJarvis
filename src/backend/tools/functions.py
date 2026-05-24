'''
    Aqui estão as funções queries que interagem diretamente com o banco de dados SQLite, 
    usando a função get_connection() definida em database.py para obter uma conexão com o banco, 
    além de funções relacionadas a tarefas, compromissos e funcionalidades específicas do processo de RAG,
''' 

# ------------ IMPORTAÇÕES --------------#

from src.backend.db.database import get_connection
import src.backend.rag.indexer as indexer
from src.backend.rag.generator import responder_rag
from src.backend.rag.connection import client
from src.backend.rag.converter import converter_para_markdown
from src.backend.rag.chunker import chunking_paragrafo
from src.backend.rag.indexer import indexar
import json
from pathlib import Path


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
    if not tarefas:
        return {"ok": True, "mensagem": "Nenhuma tarefa pendente."}
    return {"ok": True, "tarefas": tarefas}


def listar_tarefas_concluidas() -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    # seleciona apenas as tarefas que foram concluídas, ordenando pela data de prazo
    cursor.execute("SELECT * FROM tarefas WHERE concluida = 1 ORDER BY prazo DESC")
    tarefas = [dict(row) for row in cursor.fetchall()]
    conn.close()
    if not tarefas:
        return {"ok": True, "mensagem": "Nenhuma tarefa concluída."}
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
    alteradas = cursor.rowcount  # número de linhas alteradas, para verificar se a tarefa foi encontrada
    conn.close()
    if alteradas == 0:
        return {"ok": False, "mensagem": f"Tarefa '{titulo}' não encontrada."}
    return {"ok": True, "mensagem": f"Tarefa '{titulo}' concluída."}


# ---------------------- COMPROMISSOS (AGENDA) ---------------------- #

def adicionar_compromisso(titulo: str, data_hora: str, descricao: str = None, local: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    # insere um novo compromisso na tabela de compromissos, com os dados fornecidos
    cursor.execute(
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
    alterados = cursor.rowcount  # número de linhas alteradas, para verificar se o compromisso foi encontrado
    conn.close()
    if alterados == 0:
        return {"ok": False, "mensagem": f"Compromisso '{titulo}' não encontrado."}
    return {"ok": True, "mensagem": f"Compromisso '{titulo}' removido."}


def consultar_agenda(data: str = None) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    # se uma data específica for fornecida, seleciona apenas os compromissos dessa data
    # caso contrário, seleciona todos os compromissos, ordenando pela data e hora
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
    if not compromissos:
        return {"ok": True, "mensagem": "Nenhum compromisso na agenda."}
    return {"ok": True, "compromissos": compromissos}


# ---------------------- FUNÇÕES RAG ---------------------- #

def buscar_material_rag(pergunta: str) -> dict:
    if indexer.indice_faiss is None or indexer.indice_bm25 is None:
        return {"ok": False, "mensagem": "Nenhum documento foi enviado ainda. Envie um arquivo primeiro."}

    resposta, docs = responder_rag(pergunta, k=10)

    if not docs:
        return {"ok": False, "mensagem": "Nenhum material encontrado nos documentos."}

    print(f"[RAG] {len(docs)} chunks usados para responder")
    return {"ok": True, "contexto": resposta}


def planejar_estudos(pergunta: str) -> dict:
    print(f"[PLANEJAR] Combinando tarefas, agenda e documentos...")

    tarefas = listar_tarefas()
    agenda = consultar_agenda()

    contexto_rag = None
    # usa indexer.indice_faiss pelo módulo para pegar o valor atual (não congela no import)
    if indexer.indice_faiss is not None:
        resposta_rag, docs = responder_rag(pergunta, k=10)
        if docs:
            contexto_rag = resposta_rag

    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        # monta o prompt incluindo a pergunta, as tarefas pendentes, a agenda e o contexto RAG (se disponível)
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


# ---------------------- PRE CARREGAMENTO DE DATASET ---------------------- #
def precarregar_documentos(pasta: str = 'dataset') -> None:

    pasta_path = Path(pasta)
    if not pasta_path.exists():
        print(f"[PRELOAD] Pasta '{pasta}' não encontrada, ignorando.")
        return

    extensoes = {'.pdf', '.txt', '.docx'}
    arquivos = [f for f in pasta_path.iterdir() if f.suffix.lower() in extensoes]

    if not arquivos:
        print(f"[PRELOAD] Nenhum arquivo compatível em '{pasta}'.")
        return

    for arquivo in arquivos:
        print(f"[PRELOAD] Indexando {arquivo.name}...")
        markdown = converter_para_markdown(str(arquivo))
        chunks = chunking_paragrafo(markdown, source=arquivo.name)
        indexar(chunks)

    print(f"[PRELOAD] {len(arquivos)} arquivo(s) indexado(s) de '{pasta}'.")