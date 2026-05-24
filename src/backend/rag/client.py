'''
    Além disso, definimos a função processar_mensagem, que recebe a mensagem do usuário pelo frontend, 
    envia para a LLM, interpreta a resposta, chama a função correspondente e depois envia 
    o resultado de volta para a LLM formaliza-la.

'''
from datetime import datetime
import json

#importação das funções de chunking e indexação
from src.backend.rag.indexer import chunks_globais

# import do cliente para acessar a API do LLM
from src.backend.rag.connection import client

#importação das funções que compõem o tool calling
from src.backend.tools.functions import (
    adicionar_tarefa,
    listar_tarefas, #lista as tarefas pendentes -> com a coluna concluida = 0
    listar_tarefas_concluidas, #lista as tarefas concluídas -> com a coluna concluida = 1
    concluir_tarefa, # seta uma tarefa para concluida (concluida = 1)
    adicionar_compromisso, #adiciona um compromisso à agenda do usuário
    planejar_estudos, #adicionado um novo agente com contexto injetado
    remover_compromisso, #remove um compromisso da agenda do usuário
    consultar_agenda, #consulta os compromissos agendados para uma data específica ou para o futuro
    buscar_material_rag, #busca informações nos documentos enviados, para responder perguntas do usuário
    planejar_estudos #planeja estudos com base nas tarefas, compromissos e materiais disponíveis
)



mapa_funcoes = {
    "adicionar_tarefa":    adicionar_tarefa,
    "listar_tarefas":      listar_tarefas,
    "listar_tarefas_concluidas": listar_tarefas_concluidas,
    "concluir_tarefa":     concluir_tarefa,
    "consultar_agenda":    consultar_agenda,
    "buscar_material_rag": buscar_material_rag,
    "adicionar_compromisso":  adicionar_compromisso,
    "remover_compromisso": remover_compromisso,
    "planejar_estudos": planejar_estudos,
}


def processar_mensagem(mensagem: str) -> str:
    # para dar um contexto temporal para a LLM, injetamos a data e hora atuais no prompt
    #para se basear na hora de adicionar tarefas e compromissos
    data_atual = datetime.now().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M")

    # verifica se há documentos indexados
    if chunks_globais:
        info_documentos = f"Há {len(chunks_globais)} trechos de documentos indexados e disponíveis para consulta. Use buscar_material_rag para responder perguntas sobre eles."
    else:
        info_documentos = "Nenhum documento foi enviado ainda."

    # o SYSTEM_PROMPT é a mensagem de sistema que define o comportamento do agente:
    # ele conversa com o agente para indicar de que forma ele deve agir, e/ou quais 
    # informações ele deve ter em mente para responder as perguntas do usuário
    SYSTEM_PROMPT = f"""
        Você é o Jarvis, um assistente acadêmico inteligente.
        Hoje é dia {data_atual} e são {hora_atual}.

        Documentos disponíveis: {info_documentos}

        Tenha em mente que a primeira mensagem aparece ao usuário é esta, mas não precisa mencionar isso na resposta, é
        apenas para te dar contexto.: 
        "Olá! Sou seu agente virtual. Como posso ajudar você hoje? Ajudo na organização de atividades e compromissos, além de
        responder perguntas, mas respondo uma requisição por vez, tenha paciência comigo 😅"

        # Perfil e Tom de Voz
            - Seja direto, conciso e amigável.
            - Use um rico Markdown para formatar listas e destaques.
            - Cumprimentos/Despedidas: Responda de forma amigável e direta. Na despedida, 
            reforce que estará disponível quando necessário.

        # Entendimento de Intenção e Tratamento de Escopo
            - Antes de acionar qualquer ferramenta, identifique a intenção do usuário:
            - Organização/Compromissos: Use as funções de tarefas/agenda.
            - Dúvidas conceituais/conteúdo: Use as funções de busca em documentos.
            - Requisições Múltiplas: Se o usuário pedir algo que envolva mais de uma 
            função simultaneamente, informe que só processa uma requisição por vez e 
            peça para ele escolher uma ação específica.

            - Fora de Escopo: Se a solicitação não se encaixar em nenhuma função 
            disponível, responda diretamente de forma amigável (sem formato JSON) e 
            tente ajudar da melhor forma.

        # Gerenciamento de Tarefas e Agenda
            - Conclusão ou Busca de Tarefa:
            - Se o título exato não for encontrado, chame `listar_tarefas` primeiro 
            para inferir qual é a tarefa antes de declarar que não existe.
            - Se o usuário não especificar o título ao pedir para concluir, tente 
            inferir pelo contexto da conversa. Se não conseguir inferir, peça o título.
            - Se, após a busca/inferência, a tarefa realmente não for encontrada, 
            responda que a tarefa não foi encontrada.
            - Consulta de Agenda: Se não for especificada uma data, retorne todos os compromissos futuros.
            - Adicionar Compromisso: Se enviado sem data e hora, assuma o dia seguinte 
            para o dia todo (sem horário específico).

        # Recuperação de Documentos (RAG)
            - Para perguntas que usem a base de conhecimento, use obrigatoriamente a função `buscar_material_rag`.
            - Se a busca inicial não trouxer resultados, tente reformular a pergunta internamente para uma nova busca.
            - Se mesmo após a reformulação nada for encontrado, responda claramente que 
            não encontrou informações relevantes nos documentos.

        Quando o usuário pedir algo, responda SEMPRE em JSON com este formato:

        Para chamar uma função:
        {{"acao": "nome_da_funcao", "params": {{"param1": "valor1"}}}}

        Para responder diretamente:
        {{"acao": "resposta_direta", "params": {{"texto": "sua resposta aqui"}}}}


        Funções disponíveis:
        - adicionar_tarefa(titulo, prazo, prioridade): adiciona uma tarefa
        - listar_tarefas(): lista tarefas pendentes
        - listar_tarefas_concluidas(): lista tarefas concluídas
        - concluir_tarefa(titulo): marca tarefa como concluída
        - consultar_agenda(data): consulta compromissos na agenda
        - adicionar_compromisso(titulo, data_hora, descricao, local): adiciona compromisso ou evento
        - remover_compromisso(titulo, data_hora): remove compromisso da agenda
        - buscar_material_rag(pergunta): busca informações nos documentos enviados 
        - planejar_estudos(pergunta): planeja estudos com base nas tarefas e materiais disponíveis
    
        """

    historico = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": mensagem}
    ]

    # para evitar loops infinitos, limitamos o número de turnos de interação com a LLM
    # Se chegar no limite, encerramos a conversa.
    MAX_TURNOS = 6

    for turno in range(MAX_TURNOS):
        resposta = client.chat.completions.create(
            model='google/gemma-3-12b-it',
            messages=historico
        )

        conteudo = resposta.choices[0].message.content.strip()
        print(f"\n=== TURNO {turno + 1} ===\n{conteudo}")

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

            # resposta direta — encerra
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

                # para as demais funções, acumula no resultados normalmente
                resultados.append({"acao": acao, "resultado": resultado})

            # acumula no histórico
            historico.append({"role": "assistant", "content": conteudo})
            historico.append({
                "role": "user",
                "content": f"Resultados: {json.dumps(resultados, ensure_ascii=False)}. Continue chamando funções se precisar de mais dados, ou responda ao usuário em JSON."
            })

        except json.JSONDecodeError:
            return conteudo

    return "Não consegui completar a operação."