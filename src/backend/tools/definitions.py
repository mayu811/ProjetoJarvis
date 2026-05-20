"""
Aqui definimos as ferramentas (tools) que o LLM pode usar, com suas descrições e parâmetros
"""

# aqui definimos as ferramentas (tools) que o LLM pode usar, com suas descrições e parâmetros, 
# e também implementamos as funções correspondentes que serão chamadas quando o LLM decidir usar uma ferramenta.

#from src.backend.rag.retriever import recuperar_hibrido

#importação das funções de consulta ao banco de dados
'''from src.backend.db.queries import (
    adicionar_tarefa,
    listar_tarefas,
    listar_tarefas_concluidas,
    concluir_tarefa,
    adicionar_compromisso,
    consultar_agenda,
    buscar_material_rag
)
'''

'''
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
                    "prazo": {"type": "string", "description": "Prazo da tarefa no formato DD/MM/AAAA. Se sem informações, assuma o dia seguinte à data atual."},
                    "prioridade": {"type": "string", "enum": ["baixa", "media", "alta"]},
                    "descricao": {"type": "string", "description": "Descrição da tarefa"}
                },
                "required": ["titulo", "prazo"]
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
            "name": "listar_tarefas_concluidas",
            "description": "Lista todas as tarefas concluídas do estudante.",
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
            "description": "Consulta os compromissos e eventos da agenda do estudante. Se vazio, retorna todos.",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "Data para consultar no formato DD/MM/AAAA. "}
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
            "name": "adicionar_compromisso",
            "description": "Marca um compromisso ou evento na agenda do estudante.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo":    {"type": "string", "description": "Título do compromisso"},
                    "data_hora": {"type": "string", "description": "Data e hora no formato DD/MM/AAAA HH:MM"},
                    "descricao": {"type": "string", "description": "Descrição do compromisso"},
                    "local":     {"type": "string", "description": "Local do compromisso"}
                },
                "required": ["titulo"]
            }
        }
    }
]
'''


# Função para buscar material relevante usando RAG
    # foi deixada apenas esta função aqui pois ela não interage com o banco de dados, 
    # enquanto as outras funções de tarefas e agenda estão em src/backend/db/queries.py 
    # para manter a organização do código.
'''def buscar_material_rag(pergunta: str) -> dict:
    resultados = recuperar_hibrido(pergunta)
    if not resultados:
        return {"ok": False, "mensagem": "Nenhum material encontrado."}
    contexto = "\n\n".join([r["texto"] for r in resultados])
    return {"ok": True, "contexto": contexto}
'''