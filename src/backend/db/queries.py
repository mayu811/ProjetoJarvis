'''
    Aqui estão as funções queries que interagem diretamente com o banco de dados SQLite, 
    usando a função get_connection() definida em database.py para obter uma conexão com o banco.

    Essas funções são chamadas pelo backend para realizar as operações solicitadas pelo usuário, como:
        adicionar tarefas,
        concluir tarefas,
        listar tarefas, 
        adicionar compromissos,
        remover compromissos,
        consultar a agenda,
        buscar material_RAG**

    Obs.:**  
    A função buscar_material_rag é uma função especial que não interage com o banco de dados, 
    mas sim com o módulo de RAG para recuperar informações relevantes dos documentos acadêmicos. 
    Ela foi colocada aqui para manter todas as funções de backend em um único arquivo, 
    mas poderia ser movida para outro módulo se desejado, isto juntamente com a importação da suas dependências.

'''

# funções para interagir com o banco de dados (SQLite)
from src.backend.db.database import get_connection


#dependencias para interagir com a função que utiliza RAG
from src.backend.rag.retriever import recuperar_hibrido
from src.backend.rag.indexer import indice_bm25
from src.backend.rag.generator import responder_rag

# ---------------------- TAREFAS ----------------------

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

# ---------------------- COMPROMISSOS ----------------------

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


'''def buscar_material_rag(pergunta: str) -> dict:
    resultados = recuperar_hibrido(pergunta)
    if not resultados:
        return {"ok": False, "mensagem": "Nenhum material encontrado."}
    contexto = "\n\n".join([r["texto"] for r in resultados])
    return {"ok": True, "contexto": contexto}'''

'''def buscar_material_rag(pergunta: str) -> dict:    

    # verifica se há documentos indexados
    # verifica ambos
    from src.backend.rag.indexer import indice_bm25, indice_faiss #novo

    if indice_bm25 is None or indice_faiss is None: #novo
        return {"ok": False, "mensagem": "Nenhum documento foi enviado ainda. Envie um arquivo primeiro."} #novo
    
    resposta, docs = responder_rag(pergunta)

    if not docs:
        return {"ok": False, "mensagem": "Nenhum material encontrado nos documentos."}

    return {"ok": True, "contexto": resposta}
'''

# ---------------------- FUNCOES RAGS ----------------------

def buscar_material_rag(pergunta: str) -> dict:
    import src.backend.rag.indexer as indexer  # importa o módulo, não a variável

    if indexer.indice_faiss is None or indexer.indice_bm25 is None:
        return {"ok": False, "mensagem": "Nenhum documento foi enviado ainda. Envie um arquivo primeiro."}

    from src.backend.rag.generator import responder_rag
    resposta, docs = responder_rag(pergunta, k=10)

    print(f"\n=== BUSCAR_MATERIAL_RAG ===")
    print(f"Resposta do generator: {resposta[:200]}")
    print(f"Docs: {len(docs)}")
    print("===\n")

    if not docs:
        return {"ok": False, "mensagem": "Nenhum material encontrado nos documentos."}

    return {"ok": True, "contexto": resposta}


def planejar_estudos(pergunta: str) -> dict:
    from src.backend.rag.indexer import indice_faiss
    from src.backend.rag.generator import responder_rag, client
    from src.backend.db.queries import listar_tarefas, consultar_agenda
    import json

    tarefas = listar_tarefas()
    agenda = consultar_agenda()

    contexto_rag = None
    if indice_faiss is not None:
        resposta_rag, docs = responder_rag(pergunta, k=10)
        if docs:
            contexto_rag = resposta_rag

    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
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