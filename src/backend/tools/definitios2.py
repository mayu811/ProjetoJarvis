"""

JSON schema de todas as tools (descrições detalhadas)

Ainda discutivel a existencia desse arquivo, mas mantém aqui por enquanto

"""

#definitios.py


import json
from src.backend.rag.retriever import recuperar_hibrido

# definição das tools no formato que a OpenAI espera
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "adicionar_tarefa",
            "description": "Adiciona uma nova tarefa acadêmica para o estudante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "Título da tarefa"},
                    "prazo": {"type": "string", "description": "Prazo da tarefa no formato DD/MM/AAAA"},
                    "prioridade": {"type": "string", "enum": ["baixa", "media", "alta"]}
                },
                "required": ["titulo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "listar_tarefas",
            "description": "Lista todas as tarefas pendentes do estudante.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "concluir_tarefa",
            "description": "Marca uma tarefa como concluída.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "Título da tarefa a concluir"}
                },
                "required": ["titulo"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "consultar_agenda",
            "description": "Consulta os compromissos e eventos da agenda do estudante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "Data para consultar no formato DD/MM/AAAA. Se vazio, retorna todos."}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buscar_material_rag",
            "description": "Busca informações nos documentos acadêmicos enviados pelo estudante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pergunta": {"type": "string", "description": "Pergunta ou tema a buscar nos documentos"}
                },
                "required": ["pergunta"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "marcar_compromisso",
            "description": "Marca um compromisso ou evento na agenda do estudante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string", "description": "Título do compromisso"},
                    "data": {"type": "string", "description": "Data do compromisso no formato DD/MM/AAAA"},
                    "hora": {"type": "string", "description": "Hora do compromisso no formato HH:MM"}
                },
                "required": ["titulo", "data", "hora"]
            }
        }
    }
]

# armazenamento em memória (substituir por banco de dados futuramente)
tarefas = []
agenda = []

# --------- implementação das funções (essas serão chamadas pelo LLM via JSON-RPC) ------------

# função para adicionar tarefa
def adicionar_tarefa(titulo: str, prazo: str = None, prioridade: str = "baixa") -> dict:
    tarefa = {"titulo": titulo, "prazo": prazo, "prioridade": prioridade, "concluida": False}
    tarefas.append(tarefa)
    return {"ok": True, "mensagem": f"Tarefa '{titulo}' adicionada com sucesso."}

# função para listar tarefas pendentes
def listar_tarefas() -> dict:
    pendentes = [t for t in tarefas if not t["concluida"]]
    if not pendentes:
        return {"ok": True, "mensagem": "Nenhuma tarefa pendente."}
    return {"ok": True, "tarefas": pendentes}

# função para concluir tarefa
def concluir_tarefa(titulo: str) -> dict:
    for t in tarefas:
        if t["titulo"].lower() == titulo.lower():
            t["concluida"] = True
            return {"ok": True, "mensagem": f"Tarefa '{titulo}' concluída."}
    return {"ok": False, "mensagem": f"Tarefa '{titulo}' não encontrada."}

# função para consultar agenda (com ou sem filtro de data)
def consultar_agenda(data: str = None) -> dict:
    if not agenda:
        return {"ok": True, "mensagem": "Nenhum compromisso na agenda."}
    if data:
        filtrados = [c for c in agenda if c.get("data") == data]
        return {"ok": True, "compromissos": filtrados}
    return {"ok": True, "compromissos": agenda}

# função para buscar material relevante usando RAG
def buscar_material_rag(pergunta: str) -> dict:
    resultados = recuperar_hibrido(pergunta)
    if not resultados:
        return {"ok": False, "mensagem": "Nenhum material encontrado."}
    contexto = "\n\n".join([r["texto"] for r in resultados])
    return {"ok": True, "contexto": contexto}

# função para marcar compromisso na agenda
def marcar_compromisso(titulo: str, data: str, hora: str) -> dict:
    compromisso = {"titulo": titulo, "data": data, "hora": hora}
    agenda.append(compromisso)
    return {"ok": True, "mensagem": f"Compromisso '{titulo}' marcado para {data} às {hora}."}
