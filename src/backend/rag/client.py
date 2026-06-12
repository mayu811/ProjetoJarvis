'''
    Define a função processar_mensagem, que recebe a mensagem do usuário pelo frontend, 
    envia para a LLM, interpreta a resposta, chama a função correspondente e retorna 
    o resultado formatado.
'''

# -------------------- IMPORTAÇÕES --------------------

from datetime import datetime
import json
import re
from src.backend.rag.indexer import chunks_globais
from src.backend.rag.generator import exercicios_ativos
from src.backend.rag.connection import client, MODEL_NAME
from src.backend.tools.functions import (
    adicionar_tarefa,       # adiciona tarefa ao banco
    listar_tarefas,         # lista tarefas pendentes (concluida = 0)
    listar_tarefas_concluidas,  # lista tarefas concluídas (concluida = 1)
    concluir_tarefa,        # marca tarefa como concluída
    adicionar_compromisso,  # adiciona compromisso à agenda
    remover_compromisso,    # remove compromisso da agenda
    consultar_agenda,       # consulta compromissos por data ou todos
    buscar_material_rag,    # busca informações nos documentos enviados
    planejar_estudos,        # planeja estudos combinando tarefas, agenda e documentos
    gerar_exercicios,       # gera exercicios combinando documentos e a tema pedido pelo usuario
    avaliar_resposta_exercicio,   # avalia o que foi respodido does exercicios
    recomendar_revisao,     # recomenda revisoes com base no que foi perguntado
)

# -------------------- VARIAVEIS GLOBAIS --------------------
# Estado para controle do modo exercício
modo_exercicio_ativo = False

# -------------------- MAPEAMENTO DE FUNÇÕES --------------------
mapa_funcoes = {
    "adicionar_tarefa":         adicionar_tarefa,
    "listar_tarefas":           listar_tarefas,
    "listar_tarefas_concluidas": listar_tarefas_concluidas,
    "concluir_tarefa":          concluir_tarefa,
    "consultar_agenda":         consultar_agenda,
    "buscar_material_rag":      buscar_material_rag,
    "adicionar_compromisso":    adicionar_compromisso,
    "remover_compromisso":      remover_compromisso,
    "planejar_estudos":         planejar_estudos,
    #funcoes de aprendizado
    "gerar_exercicios": gerar_exercicios,
    "recomendar_revisao": recomendar_revisao,
    "avaliar_resposta_exercicio": avaliar_resposta_exercicio,
}

# -------------------- FUNCOES AUXILIARES --------------------
def extrair_json(texto: str) -> dict:
    """
    Extrai o primeiro JSON válido de uma string.
    Remove blocos de código markdown e texto ao redor.
    """
    # Remove blocos de código markdown
    if "```json" in texto:
        texto = texto.split("```json")[1].split("```")[0]
    elif "```" in texto:
        texto = texto.split("```")[1].split("```")[0]
    
    texto = texto.strip()
    
    # Tenta encontrar padrão JSON
    json_pattern = r'\{[^{}]*\}'
    matches = re.findall(json_pattern, texto)
    
    if matches:
        # Pega o último JSON (geralmente o mais completo)
        texto = matches[-1]
    
    return json.loads(texto)


# -------------------- FUNÇÃO PRINCIPAL --------------------

def processar_mensagem(mensagem: str) -> str:
    '''
    Recebe a mensagem do usuário, envia para a LLM, interpreta a resposta, 
    chama a função correspondente e retorna o resultado formatado.
    '''

    global modo_exercicio_ativo

    '''
    if exercicios_ativos and "exercicios_ativos" in dir():
        # Está respondendo um exercício
        resultado = avaliar_resposta(mensagem)
        if resultado.get("continuar"):
            return resultado["mensagem"]
        else:
            exercicios_ativos = None
            return resultado["mensagem"]
    
    if mensagem.lower().startswith("gerar exercícios sobre "):
        tema = mensagem.lower().replace("gerar exercícios sobre ", "").strip()
        resultado = gerar_exercicios(tema)
        if resultado.get("ok"):
            # Ativa modo exercício
            global exercicios_ativos
            exercicios_ativos = resultado
            return resultado["mensagem"]
        return resultado.get("mensagem", "Erro ao gerar exercícios")
    '''
    if exercicios_ativos is not None:
        resultado = avaliar_resposta(mensagem)
        if resultado.get("ok"):
            # Se o exercício terminou, sai do modo
            if "Resultado final" in resultado.get("mensagem", ""):
                modo_exercicio_ativo = False
            return resultado.get("mensagem", "")
        else:
            return resultado.get("mensagem", "Erro na avaliação.")


    data_atual = datetime.now().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M")

    # verifica se há documentos indexados para informar a LLM
    if chunks_globais:
        info_documentos = f"Há {len(chunks_globais)} trechos de documentos indexados. Use buscar_material_rag para responder perguntas sobre eles."
    else:
        info_documentos = "Nenhum documento foi enviado ainda."

    # system prompt detalhado para orientar a LLM sobre o comportamento esperado
    SYSTEM_PROMPT = f"""
        Você é o Jarvis, um assistente acadêmico inteligente.
        Hoje é dia {data_atual} e são {hora_atual}.
        {info_documentos}

        # Comportamento
        - Seja direto, conciso e amigável. Use markdown para formatação.
        - Para perguntas sobre documentos → buscar_material_rag
        - Para planejamento → planejar_estudos
        - Para exercícios → gerar_exercicios
        - Para recomendações de estudo → recomendar_revisao
        - Para tarefas/agenda → funções específicas

        # Resposta
        Responda SEMPRE em JSON puro, sem texto adicional.

        Formato para chamar função:
        {{"acao": "nome_da_funcao", "params": {{"param1": "valor1"}}}}

        Formato para resposta direta:
        {{"acao": "resposta_direta", "params": {{"texto": "sua resposta aqui"}}}}

        # Funções disponíveis
        - adicionar_tarefa(titulo, prazo, prioridade)
        - listar_tarefas()
        - listar_tarefas_concluidas()
        - concluir_tarefa(titulo)
        - consultar_agenda(data)
        - adicionar_compromisso(titulo, data_hora, descricao, local)
        - remover_compromisso(titulo)
        - buscar_material_rag(pergunta)
        - planejar_estudos(pergunta)
        - gerar_exercicios(tema, qtd)
        - recomendar_revisao(assunto_consultado)

        Responda APENAS com o JSON.
    """

    # histórico da conversa
    historico = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": mensagem}
    ]

    # limita turnos para evitar loops infinitos
    MAX_TURNOS = 6

    for turno in range(MAX_TURNOS):
        resposta = client.chat.completions.create(
            model=MODEL_NAME,
            messages=historico
        )

        conteudo = resposta.choices[0].message.content.strip()
        print(f"\n[CLIENT] Turno {turno + 1}: {conteudo[:80]}...")
        
        try:
            dados = extrair_json(conteudo)

            # Verifica ações
            if "acao" in dados:
                acoes = [{"acao": dados["acao"], "params": dados.get("params", {})}]
            elif "acoes" in dados:
                acoes = dados["acoes"]
            else:
                # Tenta resposta direta
                if "texto" in dados:
                    return dados["texto"]
                elif "resposta" in dados:
                    return dados["resposta"]
                else:
                    return "Desculpe, não entendi o formato da resposta."

            # Processa primeira ação
            primeira_acao = acoes[0]

            if primeira_acao.get("acao") == "resposta_direta":
                texto_resposta = primeira_acao.get("params", {}).get("texto", "")
                return texto_resposta if texto_resposta else "Desculpe, não consegui gerar uma resposta."

            #executa acao
            acao = primeira_acao.get("acao")
            params = primeira_acao.get("params", {})

            funcao = mapa_funcoes.get(acao)
            if not funcao:
                return f"Função '{acao}' não encontrada."

            resultado = funcao(**params)

            # RAG e planejamento já vêm com resposta formulada — retorna direto
            if acao in (
                "buscar_material_rag", 
                "planejar_estudos", 
                "gerar_exercicios", 
                "recomendar_revisao"
            ):
                if resultado.get("ok"):
                    if resultado.get("modo") == "exercicio":
                        modo_exercicio_ativo = True
                    return resultado.get("contexto", resultado.get("mensagem", ""))
                else:
                    return resultado.get("mensagem", "Erro ao processar.")
                
            #funcoes de tarefas/agenda
            if "mensagem" in resultado:
                return resultado["mensagem"]
            elif "contexto" in resultado:
                return resultado["contexto"]
            else:
                return json.dumps(resultado, ensure_ascii=False)
        
        except json.JSONDecodeError:
            print(f"[CLIENT] Erro JSON: {e}")
            # Se não for JSON, retorna como texto simples
            if len(conteudo) < 500:
                return conteudo
            return "Desculpe, tive um problema ao processar sua mensagem."

    # se atingir o limite de turnos sem resposta direta, retorna a última resposta da LLM
    return "Não consegui completar a operação."