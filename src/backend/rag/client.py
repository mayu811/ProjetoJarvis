'''
    Define a função processar_mensagem, que recebe a mensagem do usuário pelo frontend, 
    envia para a LLM, interpreta a resposta, chama a função correspondente e retorna 
    o resultado formatado.
'''

# -------------------- IMPORTAÇÕES --------------------

from datetime import datetime
import json

from src.backend.rag.indexer import chunks_globais
from src.backend.rag.connection import client
from src.backend.tools.functions import (
    adicionar_tarefa,       # adiciona tarefa ao banco
    listar_tarefas,         # lista tarefas pendentes (concluida = 0)
    listar_tarefas_concluidas,  # lista tarefas concluídas (concluida = 1)
    concluir_tarefa,        # marca tarefa como concluída
    adicionar_compromisso,  # adiciona compromisso à agenda
    remover_compromisso,    # remove compromisso da agenda
    consultar_agenda,       # consulta compromissos por data ou todos
    buscar_material_rag,    # busca informações nos documentos enviados
    planejar_estudos        # planeja estudos combinando tarefas, agenda e documentos
)

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
}

# -------------------- FUNÇÃO PRINCIPAL - processar_mensagem --------------------
def processar_mensagem(mensagem: str) -> str:
    '''
    Recebe a mensagem do usuário, envia para a LLM, interpreta a resposta, chama a função correspondente e retorna o resultado formatado.
     - mensagem: string com a pergunta ou comando do usuário
     - Retorna: string com a resposta final para o frontend
    '''

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

        # Perfil e Tom de Voz
        - Seja direto, conciso e amigável. Use markdown para formatar listas e destaques.
        - Cumprimentos/Despedidas: Responda de forma amigável e direta. Na despedida, reforce disponibilidade.

        # Entendimento de Intenção
        - Organização/Compromissos → funções de tarefas/agenda.
        - Dúvidas conceituais/conteúdo → buscar_material_rag.
        - Planejamento combinando agenda, tarefas e documentos → planejar_estudos.
        - Fora de escopo → resposta_direta amigável.

        # Gerenciamento de Tarefas e Agenda
        - Tarefa não encontrada pelo título exato → chame listar_tarefas primeiro para inferir.
        - Sem título ao concluir → tente inferir pelo contexto; se não conseguir, peça o título.
        - Consulta de agenda sem data → retorne todos os compromissos.
        - Compromisso sem data/hora → assuma o dia seguinte às 00:00.
        - Tarefa sem prazo → assuma o dia seguinte.

        # Recuperação de Documentos (RAG)
        - Use obrigatoriamente buscar_material_rag para perguntas sobre documentos enviados.
        - Se não encontrar resultados, reformule a pergunta internamente e tente novamente.

        Responda SEMPRE em JSON:

        Para chamar uma função:
        {{"acao": "nome_da_funcao", "params": {{"param1": "valor1"}}}}

        Para responder diretamente:
        {{"acao": "resposta_direta", "params": {{"texto": "sua resposta aqui"}}}}

        Funções disponíveis:
        - adicionar_tarefa(titulo, prazo, prioridade)
        - listar_tarefas()
        - listar_tarefas_concluidas()
        - concluir_tarefa(titulo)
        - consultar_agenda(data)
        - adicionar_compromisso(titulo, data_hora, descricao, local)
        - remover_compromisso(titulo)
        - buscar_material_rag(pergunta)
        - planejar_estudos(pergunta)

        Responda APENAS com o JSON, sem texto adicional.
    """

    # histórico de mensagens para a LLM, iniciando com o system prompt e a mensagem do usuário
    historico = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": mensagem}
    ]

    # limita turnos para evitar loops infinitos
    MAX_TURNOS = 6

    for turno in range(MAX_TURNOS):
        resposta = client.chat.completions.create(
            model='google/gemma-3-12b-it',
            messages=historico
        )

        conteudo = resposta.choices[0].message.content.strip()
        print(f"\n[CLIENT] Turno {turno + 1}: {conteudo[:120]}")

        # remove possíveis blocos de código e formatações para extrair o JSON puro
        if conteudo.startswith("```"):
            conteudo = conteudo.split("```")[1]
            if conteudo.startswith("json"):
                conteudo = conteudo[4:]

        try:
            dados = json.loads(conteudo)

            # normaliza para aceitar "acao" ou "acoes"
            if "acao" in dados and "acoes" not in dados:
                acoes = [{"acao": dados["acao"], "params": dados.get("params", {})}]
            else:
                acoes = dados.get("acoes", [])

            # resposta direta — encerra o loop
            if acoes and acoes[0].get("acao") == "resposta_direta":
                return acoes[0]["params"].get("texto", conteudo)

            # executa todas as ações do turno
            resultados = []
            for item in acoes:
                acao = item.get("acao")
                params = item.get("params", {})

                funcao = mapa_funcoes.get(acao)
                if not funcao:
                    resultados.append({"acao": acao, "erro": f"Função '{acao}' não encontrada."})
                    continue

                resultado = funcao(**params)

                # RAG e planejamento já vêm com resposta formulada — retorna direto
                if acao in ("buscar_material_rag", "planejar_estudos"):
                    if resultado.get("ok"):
                        return resultado.get("contexto")
                    else:
                        return resultado.get("mensagem")

                # demais funções acumulam no histórico
                resultados.append({"acao": acao, "resultado": resultado})

            # acumula resultados no histórico para o próximo turno
            historico.append({"role": "assistant", "content": conteudo})
            historico.append({
                "role": "user",
                "content": f"Resultados: {json.dumps(resultados, ensure_ascii=False)}. Continue ou responda ao usuário em JSON."
            })
        
        except json.JSONDecodeError:
            return conteudo

    # se atingir o limite de turnos sem resposta direta, retorna a última resposta da LLM
    return "Não consegui completar a operação."