'''
    Módulo de geração de respostas usando RAG (Retrieval-Augmented Generation).
    Recebe a pergunta do usuário, recupera os documentos relevantes usando o retriever híbrido (BM25 + embedding)
'''

# ---------------------- IMPORTAÇÕES --------------------------
from src.backend.rag.retriever import recuperar_hibrido
from src.backend.rag.connection import client, MODEL_NAME
import src.backend.rag.indexer as indexer
import json
import re
# ---------------------- VARIAVEIS GLOBAIS --------------------------
exercicios_ativos = None

# ---------------------- FUNCOES AUXILIARES --------------------------
def _buscar_contexto_rag(pergunta: str, k: int = 5) -> str:
    """
    Busca contexto via RAG, caso o índice já tenha sido construído.
    Retorna string vazia se não houver índice ou documentos relevantes.
    """
    if indexer.indice_faiss is None:
        return ""
 
    resposta_rag, docs = responder_rag(pergunta, k=k)
    return resposta_rag if docs else ""

def _chamar_llm_json(prompt: str, temperature: float = 0.5, max_tokens: int = 500) -> dict:
    """
    Chama o LLM esperando uma resposta em JSON, removendo possíveis
    blocos de markdown (```json ... ```) antes de parsear.
    """
    resp = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens
    )
 
    conteudo = resp.choices[0].message.content.strip()

    if "```json" in conteudo:
        conteudo = conteudo.split("```json")[1].split("```")[0]
    elif "```" in conteudo:
        conteudo = conteudo.split("```")[1].split("```")[0]

    conteudo = conteudo.strip()
    conteudo = conteudo.replace('\t', ' ')        # tabs viram espaço
    conteudo = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', conteudo)  # escapa barras soltas
 
    return json.loads(conteudo.strip())
 

# ---------------------- FUNÇÃO COM RAG --------------------------
def responder_rag(pergunta: str, k: int = 5, alpha: float = 0.5) -> tuple:
    '''
        Função principal do RAG:
        1. Recupera os k chunks mais relevantes
        2. Monta o prompt com o contexto usando o chat template do Qwen2.5
        3. Gera a resposta com o LLM
    '''
    docs = recuperar_hibrido(pergunta, k=k, alpha=alpha)

    if not docs:
        print(f"\n[GENERATOR] Saída: nenhum documento encontrado")
        return "Não encontrei informações relevantes nos documentos enviados.", docs

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

    try:
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1000
        )

        resposta = resp.choices[0].message.content
        print(f"[GENERATOR] Fontes usadas: {sources_used}")
        print(f"[GENERATOR] Resposta gerada: {len(resposta)} caracteres")

        return resposta, docs
    except Exception as e:
        print(f"\n[GENERATOR] ERRO: {e}")
        return f"Erro ao gerar resposta: {str(e)}", docs


def planejar_estudos_com_rag(pergunta: str, tarefas: dict, agenda: dict) -> str:
    """
    Gera plano de estudos combinando RAG + tarefas + agenda
    """

    # Busca contexto dos documentos
    contexto_rag = _buscar_contexto_rag(pergunta, k=5)

    # Gera plano usando LLM
    resp = client.chat.completions.create(
        model=MODEL_NAME,
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
                {json.dumps(tarefas, ensure_ascii=False, indent=2)}

                Agenda:
                {json.dumps(agenda, ensure_ascii=False, indent=2)}

                Conteúdo dos documentos relevantes:
                {contexto_rag or "Nenhum documento enviado."}

                Monte um plano de estudos claro, com etapas específicas e prioridades.
                """
            }
        ],
        temperature=0.5,
        max_tokens=1500
    )
    
    return resp.choices[0].message.content

def gerar_exercicios_com_rag(tema: str, qtd: int = 3) -> dict:
    """
    Gera exercícios sobre um tema e avalia as respostas do usuário.
    Funcionalidade interativa de aprendizado.
    """
    global exercicios_ativos
    
    # Busca contexto dos documentos
    contexto = _buscar_contexto_rag(tema, k=5)
    
    # Gera exercicios usando LLM
    prompt_exercicios = f"""Você é um professor acadêmico. Crie {qtd} exercícios sobre "{tema}".
        Contexto disponível (use como base):
        {contexto if contexto else "Use seu conhecimento geral."}

        Formato de resposta (JSON puro):
        {{
            "titulo": "Exercícios sobre {tema}",
            "questoes": [
                {{
                    "id": 1,
                    "pergunta": "texto da pergunta",
                    "resposta_esperada": "palavras-chave ou conceitos esperados"
                }}
            ]
        }}

        REGRAS:
        - As perguntas devem testar compreensão, não decoreba
        - Inclua um mix de conceitos teóricos e exemplos práticos
        - A resposta_esperada deve conter palavras-chave para avaliação
        """

    try:
        exercicios = _chamar_llm_json(prompt_exercicios, temperature=0.7, max_tokens=1000)

        # Armazena exercícios em sessão (usando variável global simples)
        exercicios_ativos = {
            "tema": tema,
            "questoes": exercicios["questoes"],
            "indice_atual": 0,
            "respostas": []
        }

        # Retorna a primeira pergunta
        primeira_questao = exercicios["questoes"][0]

        return {
            "ok": True,
            "modo": "exercicio",
            "mensagem": f"📝 **{exercicios['titulo']}**\n\n"
                       f"Responda uma pergunta por vez.\n\n"
                       f"**Pergunta 1/{len(exercicios['questoes'])}:**\n"
                       f"{primeira_questao['pergunta']}\n\n"
                       f"(Digite sua resposta para continuar)",
                        "questao_atual": primeira_questao,
                        "total_questoes": len(exercicios["questoes"])
            }
    except Exception as e:
        print(f"[EXERCICIOS] Erro ao gerar exercícios: {e}")
        return {"ok": False, "mensagem": f"Erro ao gerar exercícios: {str(e)}"}
    
def avaliar_resposta_com_rag(resposta_usuario: str) -> dict:
    """
    Avalia a resposta do usuário e avança para próxima questão.
    """
    global exercicios_ativos
    
    if not exercicios_ativos:
        return {"ok": False, "mensagem": "Nenhum exercício ativo. Use 'gerar exercícios sobre [tema]' primeiro."}
    
    questao_atual = exercicios_ativos["questoes"][exercicios_ativos["indice_atual"]]

    prompt_avaliacao = f"""
        Avalie a resposta do aluno para a seguinte questão.

        QUESTÃO: {questao_atual['pergunta']}
        RESPOSTA ESPERADA (palavras-chave): {questao_atual['resposta_esperada']}
        RESPOSTA DO ALUNO: {resposta_usuario}

        Responda em JSON:
        {{
            "correta": true/false,
            "feedback": "texto explicativo (2-3 linhas)",
            "dica": "dica para melhorar (se incorreta)"
        }}
    """

    try:
        avaliacao = _chamar_llm_json(prompt_avaliacao, temperature=0.3, max_tokens=300)
        
        # Registra a resposta
        exercicios_ativos["respostas"].append({
            "pergunta": questao_atual["pergunta"],
            "resposta": resposta_usuario,
            "correta": avaliacao["correta"],
            "feedback": avaliacao["feedback"]
        })
        
        # Avança para próxima questão
        exercicios_ativos["indice_atual"] += 1
        
        # Verifica se acabou
        if exercicios_ativos["indice_atual"] >= len(exercicios_ativos["questoes"]):
            # Calcula pontuação
            acertos = sum(1 for r in exercicios_ativos["respostas"] if r["correta"])
            total = len(exercicios_ativos["respostas"])
            
            resumo = f"\n\n📊 **Resultado final:** {acertos}/{total} acertos\n\n"
            for i, r in enumerate(exercicios_ativos["respostas"], 1):
                status = "✅" if r["correta"] else "❌"
                resumo += f"{status} **Q{i}:** {r['feedback']}\n"
            
            exercicios_ativos = None  # Limpa sessão
            return {"ok": True, "mensagem": resumo}
        
        # Próxima questão
        proxima = exercicios_ativos["questoes"][exercicios_ativos["indice_atual"]]
        return {
            "ok": True,
            "mensagem": f"{avaliacao['feedback']}\n\n"
                       f"**Próxima pergunta ({exercicios_ativos['indice_atual'] + 1}/{len(exercicios_ativos['questoes'])}):**\n"
                       f"{proxima['pergunta']}",
            "continuar": True
        }
        
    except Exception as e:
        print(f"[APRENDIZADO] Erro ao avaliar: {e}")
        return {"ok": False, "mensagem": f"Erro na avaliação: {str(e)}"}

def recomendar_revisao_com_rag(assunto_consultado: str) -> dict:
    """
    Funcionalidade passiva de aprendizado.
    Recomenda tópicos relacionados para revisão com base na pergunta do usuário.
    """
    #busca contexto
    contexto = _buscar_contexto_rag(f"conceitos relacionados a {assunto_consultado}", k=3)
    
    prompt_recomendacao = f"""
        Com base na consulta do usuário sobre "{assunto_consultado}", 
        sugira 3 tópicos relacionados que seriam úteis para revisão.
        Não responda usando markdown.

        Contexto disponível (se houver):
        {contexto if contexto else "Use seu conhecimento geral"}

        Responda em JSON:
        {{
            "topicos": [
                "tópico 1",
                "tópico 2", 
                "tópico 3"
            ],
            "justificativa": "por que esses tópicos são relevantes",
            "pergunta_sugerida": "uma pergunta que o usuário pode fazer para aprender mais"
        }}
    """
    try:
        recomendacao = _chamar_llm_json(prompt_recomendacao, temperature=0.5, max_tokens=400)
        
        mensagem = (            
            f'💡 Sugestão de revisão para "{assunto_consultado}":\n'
            f'Tópicos relacionados:\n'
            f'• {recomendacao["topicos"][0]}\n'
            f'• {recomendacao["topicos"][1]}\n'
            f'• {recomendacao["topicos"][2]}\n\n'
            f'Por que revisar? {recomendacao["justificativa"]}\n\n'
            f'❓ Que tal: {recomendacao["pergunta_sugerida"]}\n\n'
            f'Digite "gerar exercícios sobre [tópico]" para praticar!'
        )
        
        return {"ok": True, "contexto": mensagem}
        
    except Exception as e:
        print(f"[APRENDIZADO] Erro ao recomendar: {e}")
        return {"ok": False, "mensagem": ""}