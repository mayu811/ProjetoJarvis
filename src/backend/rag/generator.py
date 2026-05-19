#geração final de resposta usando LLM + contexto relevante

import json
from src.backend.rag.retriever import recuperar_hibrido
from openai import OpenAI

client = OpenAI(base_url='https://llm.liaufms.org/v1/gemma-3-12b-it', api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A')


#print(resp.choices[0].message.content)


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


def responder_rag(pergunta, k=3, alpha=0.6, max_tokens=512):
    """
    Função principal do RAG:
      1. Recupera os k chunks mais relevantes
      2. Monta o prompt com o contexto usando o chat template do Qwen2.5
      3. Gera a resposta com o LLM
    """
    # ── Passo 1: Recuperação ──
    docs = recuperar_hibrido(pergunta, k=k, alpha=alpha)

    # ── Passo 2: Construção do prompt via chat template ──
    conteudo = construir_prompt(pergunta, docs)
    messages = [{"role": "user", "content": conteudo}]

    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        messages=messages,
    )

    return resp.choices[0].message.content, docs

#print("Pipeline RAG pronto!")