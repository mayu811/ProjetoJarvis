'''
    Módulo de geração de respostas usando RAG (Retrieval-Augmented Generation).
    Recebe a pergunta do usuário, recupera os documentos relevantes usando o retriever híbrido ( BM25 + embedding (dense))

'''

# ---------------------- IMPORTAÇÕES --------------------------
from src.backend.rag.retriever import recuperar_hibrido
from src.backend.rag.connection import client


#
def responder_rag(pergunta: str, k: int = 10, alpha: float = 0.6) -> tuple:
    '''
        Função principal do RAG:
        1. Recupera os k chunks mais relevantes
        2. Monta o prompt com o contexto usando o chat template do Qwen2.5
        3. Gera a resposta com o LLM
    '''
    docs = recuperar_hibrido(pergunta, k=k, alpha=alpha)

    if not docs:
        print(f"[GENERATOR] Saída: nenhum documento encontrado")
        return "Nenhum material encontrado nos documentos.", docs

    # monta contexto com source explícito
    contexto = "\n\n".join([
        f"[Documento: {d['source']}]\n{d['texto']}"
        for d in docs
    ])

    # sources usados
    sources = {}
    for d in docs:
        sources[d['source']] = sources.get(d['source'], 0) + 1

    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        messages=[
            {
                "role": "system",
                "content": """Você é um assistente especializado em responder perguntas com base em documentos acadêmicos.
                Regras:
                - Responda APENAS com base nos trechos fornecidos.
                - Se não encontrar a informação nos trechos, diga exatamente: "Não encontrei essa informação nos documentos enviados."
                - NUNCA invente informações.
                - Responda em português usando markdown."""
            },
            {
                "role": "user",
                "content": f"Trechos dos documentos:\n\n{contexto}\n\nPergunta: {pergunta}"
            }
        ]
    )

    resposta = resp.choices[0].message.content
    print(f"[GENERATOR] sources: {sources} | {len(resposta)} chars")

    return resposta, docs