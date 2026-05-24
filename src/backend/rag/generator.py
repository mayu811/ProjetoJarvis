#geração final de resposta usando LLM + contexto relevante

import json
from src.backend.rag.retriever import recuperar_hibrido
from openai import OpenAI

client = OpenAI(base_url='https://llm.liaufms.org/v1/gemma-3-12b-it', api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A')


#print(resp.choices[0].message.content)

# função para construir o prompt a partir da pergunta e dos documentos recuperados
def construir_prompt(pergunta, docs):
    """
    Monta o conteúdo da mensagem do usuário enviada ao LLM.
    O modelo deve responder APENAS com base no contexto fornecido.
    """

    contexto = "\n\n".join(
        [f"Trecho {i+1}:\n{d['texto']}" for i, d in enumerate(docs)]
    )
    return (
        "Responda em portugues usando apenas o contexto abaixo. "
        "Se nao houver informacao suficiente, diga: nao encontrado no contexto.\n\n"
        f"Contexto:\n{contexto}\n\n"
        f"Pergunta: {pergunta}"
    )

# função principal para gerar resposta usando RAG
def responder_rag(pergunta: str, k: int = 10, alpha: float = 0.6) -> tuple:
    docs = recuperar_hibrido(pergunta, k=k, alpha=alpha)

    if not docs:
        return "Nenhum material encontrado nos documentos.", docs

    # monta contexto com source explícito
    contexto = "\n\n".join([
        f"[Documento: {d['source']}]\n{d['texto']}"
        for d in docs
    ])

    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        messages=[
            {
                "role": "system",
                "content": """Você é um assistente especializado em responder perguntas com base em documentos acadêmicos.                    Regras:
                    - Responda APENAS com base nos trechos fornecidos.
                    - Se a informação vier de documentos diferentes, deixe claro qual documento contém cada informação.
                    - Se não encontrar a informação nos trechos, diga exatamente: "Não encontrei essa informação nos documentos enviados."
                    - Nunca invente informações.
                    - Responda em português usando markdown."""
            },
            {
                "role": "user",
                "content": f"Trechos dos documentos:\n\n{contexto}\n\nPergunta: {pergunta}"
            }
        ]
    )

    return resp.choices[0].message.content, docs