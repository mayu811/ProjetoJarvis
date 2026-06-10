'''
    Módulo de geração de respostas usando RAG (Retrieval-Augmented Generation).
    Recebe a pergunta do usuário, recupera os documentos relevantes usando o retriever híbrido ( BM25 + embedding (dense))

'''

# ---------------------- IMPORTAÇÕES --------------------------
from src.backend.rag.retriever import recuperar_hibrido
from src.backend.rag.connection import client


#
def responder_rag(pergunta: str, k: int = 5, alpha: float = 0.5) -> tuple:
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

    '''
    # monta contexto com source explícito
    contexto = "\n\n".join([
        f"[Documento: {d['source']}]\n{d['texto']}"
        for d in docs
    ])
    '''

    # Monta contexto de forma mais limpa
    contexto_parts = []
    for i, d in enumerate(docs, 1):
        contexto_parts.append(f"📄 Fonte {i} ({d['source']}):\n{d['texto']}")
    
    contexto = "\n\n---\n\n".join(contexto_parts)

    # sources usados
    sources_used = {}
    for d in docs:
        sources_used[d['source']] = sources_used.get(d['source'], 0) + 1
    
    prompt = f"""Você é um assistente acadêmico. Responda com base APENAS nos trechos fornecidos.

    {contexto}

    PERGUNTA: {pergunta}

    REGRAS:
    1. Use SOMENTE as informações dos trechos acima
    2. Se não encontrar a resposta, diga "Não encontrei essa informação nos documentos enviados"
    3. Cite quais fontes você usou (ex: "Segundo o arquivo X.pdf...")
    4. Seja direto e objetivo, use markdown para formatação

    RESPOSTA:"""

    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,  # menor = mais factual
        max_tokens=1000
    )
    try:

        resp = client.chat.completions.crete(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.3,
            max_tokens=1000
        )
        
        
        


        '''
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
        '''

        resposta = resp.choices[0].message.content
        #print(f"[GENERATOR] sources: {sources} | {len(resposta)} chars")
        print(f"[GENERATOR] Fontes usadas: {sources_used}")
        print(f"[GENERATOR] Resposta gerada: {len(resposta)} caracteres")

        return resposta, docs
    except Exception as e:
        print(f"[GENERATOR] ERRO: {e}")
        return f"Erro ao gerar resposta: {str(e)}", docs