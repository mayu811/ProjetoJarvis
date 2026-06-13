'''
    Aqui estão as funções queries que interagem diretamente com o banco de dados SQLite, 
    usando a função get_connection() definida em database.py para obter uma conexão com o banco, 
    além de funções relacionadas a tarefas, compromissos e funcionalidades específicas do processo de RAG,
''' 

# ------------ IMPORTAÇÕES --------------#
import json
from src.backend.rag.connection import client, MODEL_NAME
from src.backend.db.database import get_connection
import src.backend.rag.indexer as indexer
from src.backend.rag.generator import (
    responder_rag, 
    planejar_estudos_com_rag, 
    avaliar_resposta_com_rag,
    recomendar_revisao_com_rag, 
    gerar_exercicios_com_rag
)

# ---------------------- FUNCOES DE TAREFAS ---------------------- #

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

# funcao de formatacao
def _formatar_tarefas(tarefas: list) -> str:
    if not tarefas:
        return "📋 Nenhuma tarefa encontrada."

    texto = "📋 **Suas tarefas:**\n\n"
    for t in tarefas:
        status = "✅" if t.get('concluida') else "⏳"
        texto += f"{status} **{t['titulo']}**\n"
        texto += f"  ⏰ Prazo: {t.get('prazo', 'Sem prazo')} | ⭐ Prioridade: {t.get('prioridade', 'baixa')}\n\n"
    return texto

# ---------------------- FUNCOES DE COMPROMISSOS (AGENDA) ---------------------- #

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

#funcao de formatacao
def _formatar_compromissos(compromissos: list) -> str:
    if not compromissos:
        return "📅 Nenhum compromisso na agenda."

    texto = "📅 **Sua agenda:**\n\n"
    for c in compromissos:
        texto += f"• **{c['titulo']}**\n"
        texto += f"  📍 {c.get('local', 'Sem local')} | 📅 {c.get('data_hora', 'Data não informada')}\n"
        if c.get('descricao'):
            texto += f"  📝 {c['descricao']}\n"
        texto += "\n"
    return texto



# ---------------------- FUNÇÕES QUE USAM RAG ---------------------- #

def buscar_material_rag(pergunta: str) -> dict:
    if indexer.indice_faiss is None or indexer.indice_bm25 is None:
        return {"ok": False, "mensagem": "Nenhum documento foi enviado ainda. Envie um arquivo primeiro."}

    resposta, docs = responder_rag(pergunta, k=10)

    if not docs:
        return {"ok": False, "mensagem": "Nenhum material encontrado nos documentos."}

    print(f"[RAG] {len(docs)} chunks usados para responder")
    return {"ok": True, "contexto": resposta}


def planejar_estudos(pergunta: str) -> dict:
    """Planeja estudos combinando tarefas, agenda e documentos"""
    print(f"[PLANEJAR] Combinando tarefas, agenda e documentos...")

    tarefas = listar_tarefas()
    agenda = consultar_agenda()

    try:
        plano = planejar_estudos_com_rag(pergunta, tarefas, agenda)
        return {"ok": True, "contexto": plano}
    except Exception as e:
        print(f"[PLANEJAR] ERRO: {e}")
        return {"ok": False, "mensagem": f"Erro no planejamento: {str(e)}"}


def gerar_exercicios(tema: str, qtd: int = 5) -> dict:
    """
    Funcionalidade interativa de aprendizado.
    Gera exercicios sobre um tema
    
    Args:
        tema (str): _description_
        num_questoes (int, optional): _description_. Defaults to 5.

    Returns:
        dict: _description_
    """

    print(f"[EXERCICIOS] Gerando exercícios sobre: {tema}")

    try:
        return gerar_exercicios_com_rag(tema, qtd)
    except Exception as e:
        print(f"[EXERCICIOS] ERRO: {e}")
        return {"ok": False, "mensagem": f"Erro no geramento: {str(e)}"}


def avaliar_resposta_exercicio(resposta_usuario: str) -> dict:
    """
    Avalia a resposta do usuario e avança para a próxima questão.

    Args:
        resposta_usuario (str): Resposta que ele deu para um dos exercicios gerados

    Returns:
        dict: 
    """
    
    print(f"[AVALIACAO] Avaliando resposta...")

    try:
        return avaliar_resposta_com_rag(resposta_usuario)
    except Exception as e:
        print(f"[AVALIACAO] ERRO: {e}")
        return {"ok": False, "mensagem": f"Erro na avaliacao: {str(e)}"}


def recomendar_revisao(assunto_consultado: str) -> dict:
    """
    Recomenda tópicos relacionados para revisão com base na pergunta do usuário.
    Funcionalidade passiva de aprendizado.
    """
        
    print(f"[RECOMENDACAO] Gerando recomendações para: {assunto_consultado}")

    try:
        return recomendar_revisao_com_rag(assunto_consultado)
    except Exception as e:
        print(f"[RECOMENDACAO] ERRO: {e}")
        return {"ok": False, "mensagem": ""}