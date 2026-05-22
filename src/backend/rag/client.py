'''
    Aqui estabelecemos a conexão com a API da LLM
    Além disso, definimos a função processar_mensagem, que recebe a mensagem do usuário, 
    envia para a LLM, interpreta a resposta, chama a função correspondente e depois envia 
    o resultado de volta para a LLM formaliza-la.

'''

#chama a API do LLM para obter respostas
from datetime import datetime
import json
from openai import OpenAI


#importação das funções que compõem o tool calling
from src.backend.db.queries import (
    adicionar_tarefa, #adiciona uma tarefa à lista de tarefas pendentes
    listar_tarefas, #lista as tarefas pendentes -> com a coluna concluida = 0
    listar_tarefas_concluidas, #lista as tarefas concluídas -> com a coluna concluida = 1
    concluir_tarefa, # seta uma tarefa para concluida (concluida = 1)
    adicionar_compromisso, #adiciona um compromisso à agenda do usuário
    planejar_estudos, #adicionado um novo agente com contexto injetado
    remover_compromisso, #remove um compromisso da agenda do usuário
    consultar_agenda, #consulta os compromissos agendados para uma data específica ou para o futuro
    buscar_material_rag #busca informações nos documentos enviados, para responder perguntas do usuário
)


# cliente para acessar a API do LLM (configurado para usar o modelo Gemma-3.12b-it hospedado no LIA)
client = OpenAI(
    base_url='https://llm.liaufms.org/v1/gemma-3-12b-it',
    api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A'
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
    "planejar_estudos": planejar_estudos
    #"importar_agenda_pdf": importar_agenda_pdf # função para extrair compromissos de um PDF de agenda, ainda não implementada
    # se tiver mais funções, adicionar aqui
}


def processar_mensagem(mensagem: str) -> str:
    data_atual = datetime.now().strftime("%d/%m/%Y")
    hora_atual = datetime.now().strftime("%H:%M")

    # verifica se há documentos indexados
    from src.backend.rag.indexer import chunks_globais
    if chunks_globais:
        info_documentos = f"Há {len(chunks_globais)} trechos de documentos indexados e disponíveis para consulta. Use buscar_material_rag para responder perguntas sobre eles."
    else:
        info_documentos = "Nenhum documento foi enviado ainda."

    SYSTEM_PROMPT = f"""
        Você é o Jarvis, um assistente acadêmico inteligente.
        Hoje é dia {data_atual} e são {hora_atual}.


        Documentos disponíveis: {info_documentos}

        Tenha em mente que a primeira mensagem aparece ao usuário é esta, mas não precisa mencionar isso na resposta, é apenas para te dar contexto.: 
        "Olá! Sou seu agente virtual. Como posso ajudar você hoje? 
        Ajudo na organização de atividades e compromissos, além de
        responder perguntas, mas respondo uma 
        requisição por vez, tenha paciência comigo 😅"

        Regras de comportamento:
        - Se o usuário cumprimentar, responda de forma amigável e diretamente.
        - Se o usuário se despedir, responda de forma amigável e diretamente, falando que estará disponível quando necessário.
        - Seja direto e conciso. Evite frases longas e explicações desnecessárias.
        - Nunca diga "Hum", "Parece que", "Talvez". Vá direto ao ponto.
        - Ao concluir ou buscar uma tarefa, se não encontrar pelo título exato, chame listar_tarefas primeiro para ver as tarefas existentes e inferir qual o usuário se refere antes de dizer que não encontrou.
        - Ao confirmar uma ação, seja breve: "Tarefa concluída!" em vez de parágrafos explicativos.
        - Use markdown para formatar listas e destaques.
        - Sempre responda em português, mesmo que a pergunta seja em outro idioma.
        - Se o usuário fizer uma pergunta que não se encaixe nas funções disponíveis, responda diretamente com uma resposta amigável, sem JSON, e tente ajudar da melhor forma possível.
        - Se o usuário pedir algo que envolva mais de uma função, responda que só pode processar uma requisição por vez e peça para ele escolher uma ação específica.
        - Se o usuário pedir para concluir uma tarefa sem especificar o título, tente inferir qual tarefa ele se refere com base no contexto da conversa. Se não conseguir inferir, peça para ele especificar o título da tarefa a concluir.
        - Se o usuário pedir para concluir uma tarefa e o título não for encontrado, responda que a tarefa não foi encontrada.
        - Se o usuário pedir para consultar a agenda sem especificar uma data, retorne todos os compromissos futuros.
        - Se o usuário pedir para adicionar um compromisso sem data e hora, assuma o dia seguinte para o dia todo, ao invés de uma hora específica.
        - Se o usuário fizer uma pergunta que possa ser respondida com base nos documentos enviados, use a função buscar_material_rag para obter as informações relevantes e responda com base nisso. Se não encontrar nada, responda que não encontrou informações relevantes.


        Glossário (linguagem ubiquitária para o LLM entender melhor as intenções do usuário):
        - "Tarefa": atividade acadêmica a ser realizada, como "estudar para prova", "fazer trabalho", "ler artigo", etc.
        - "Compromisso": evento agendado com data e hora, como "reunião com grupo de estudo", "aula de reforço", "consulta com professor", etc.
        - "Concluir tarefa": marcar uma tarefa como concluída, indicando que foi realizada.
        - "Consultar agenda": verificar os compromissos agendados para uma data específica ou para o futuro.
        - "Buscar material": procurar informações relevantes nos documentos enviados, para responder perguntas do usuário.
        - "Evento": equivalente a um compromisso.


        Quando o usuário pedir algo, responda SEMPRE em JSON com este formato:

        Para chamar uma função:
        {{"action": "nome_da_funcao", "params": {{"param1": "valor1"}}}}

        Para responder diretamente:
        {{"action": "resposta_direta", "params": {{"texto": "sua resposta aqui"}}}}


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
    


        Responda APENAS com o JSON, sem texto adicional.
        """

    historico = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": mensagem}
    ]

    # para evitar loops infinitos, limitamos o número de turnos de interação com a LLM. Se chegar no limite, encerramos a conversa.
    MAX_TURNOS = 6

    for turno in range(MAX_TURNOS):
        resp = client.chat.completions.create(
            model='google/gemma-3-12b-it',
            messages=historico
        )

        conteudo = resp.choices[0].message.content.strip()
        print(f"\n=== TURNO {turno + 1} ===\n{conteudo}")

        if conteudo.startswith("```"):
            conteudo = conteudo.split("```")[1]
            if conteudo.startswith("json"):
                conteudo = conteudo[4:]

        try:
            dados = json.loads(conteudo)

            # normaliza para aceitar "action" ou "actions"
            if "action" in dados and "actions" not in dados:
                actions = [{"action": dados["action"], "params": dados.get("params", {})}]
            else:
                actions = dados.get("actions", [])

            # resposta direta — encerra
            if actions and actions[0].get("action") == "resposta_direta":
                return actions[0]["params"].get("texto", conteudo)

            # executa todas as ações do turno
            resultados = []
            for item in actions:
                action = item.get("action")
                params = item.get("params", {})

                funcao = mapa_funcoes.get(action)
                if not funcao:
                    resultados.append({"action": action, "erro": f"Função '{action}' não encontrada."})
                    continue

                resultado = funcao(**params)

                '''# RAG já vem com resposta formulada
                if action == "buscar_material_rag":
                    resultados.append({"action": action, "resultado": resultado.get("contexto") if resultado.get("ok") else resultado.get("mensagem")})
                else:
                    resultados.append({"action": action, "resultado": resultado})'''
                
                # RAG e planejamento já vêm com resposta formulada — retorna direto
                if action in ("buscar_material_rag", "planejar_estudos"):
                    if resultado.get("ok"):
                        return resultado.get("contexto")
                    else:
                        return resultado.get("mensagem")

                # para as demais funções, acumula no resultados normalmente
                resultados.append({"action": action, "resultado": resultado})

            # acumula no histórico
            historico.append({"role": "assistant", "content": conteudo})
            historico.append({
                "role": "user",
                "content": f"Resultados: {json.dumps(resultados, ensure_ascii=False)}. Continue chamando funções se precisar de mais dados, ou responda ao usuário em JSON."
            })

        except json.JSONDecodeError:
            return conteudo

    return "Não consegui completar a operação."