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
    adicionar_tarefa,
    listar_tarefas,
    listar_tarefas_concluidas,
    concluir_tarefa,
    adicionar_compromisso,
    remover_compromisso,
    consultar_agenda,
    buscar_material_rag
)


# cliente para acessar a API do LLM (configurado para usar o modelo Gemma-3.12b-it hospedado no LIA)
client = OpenAI(
    base_url='https://llm.liaufms.org/v1/gemma-3-12b-it',
    api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A'
)

# orientação do tempo real para o LLM, para que ele possa usar isso como contexto em suas respostas e decisões.
data_atual = datetime.now().strftime("%d/%m/%Y")
hora_atual = datetime.now().strftime("%H:%M")



# Sistema de prompt para o LLM entender como usar as funções

# obs.: foi usada o copilot para criar esse prompt, e depois 
# ajustado manualmente para ficar mais claro e direto, seguindo 
# as regras de comportamento definidas.

SYSTEM_PROMPT = f"""
Você é o Jarvis, um assistente acadêmico inteligente.
Hoje é dia {data_atual} e são {hora_atual}.

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


Responda APENAS com o JSON, sem texto adicional.
"""

# obs.: o LLM vai responder com um JSON contendo a função a ser chamada e os parâmetros, ou uma resposta direta. 
# O backend vai processar isso e chamar a função correspondente, ou retornar a resposta direta.
mapa_funcoes = {
    "adicionar_tarefa":    adicionar_tarefa,
    "listar_tarefas":      listar_tarefas,
    "listar_tarefas_concluidas": listar_tarefas_concluidas,
    "concluir_tarefa":     concluir_tarefa,
    "consultar_agenda":    consultar_agenda,
    "buscar_material_rag": buscar_material_rag,
    "adicionar_compromisso":  adicionar_compromisso,
    "remover_compromisso": remover_compromisso
}

# função para processar a mensagem do usuário
def processar_mensagem(mensagem: str) -> str:

    # primeira chamada: LLM decide qual função chamar e com quais parâmetros
    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": mensagem}
        ]
    )

    # extrai o conteúdo da resposta do LLM, que deve ser um JSON indicando a ação a ser tomada
    #o strip() é para remover espaços em branco no início e no final
    conteudo = resp.choices[0].message.content.strip()

    # tenta interpretar o conteúdo como JSON para extrair a ação e os parâmetros
    try:
        # remove blocos de código se existirem, para evitar erros de parsing JSON
        # remove blocos ```json ... ``` se existirem
        if conteudo.startswith("```"):
            # extrai o conteúdo dentro do bloco de código
            conteudo = conteudo.split("```")[1]
            # remove a palavra "json" no início, se existir
            if conteudo.startswith("json"):
                # remove a palavra "json" no início, se existir
                conteudo = conteudo[4:]

        # tenta interpretar o conteúdo como JSON
        dados = json.loads(conteudo)
        # extrai a ação e os parâmetros do JSON
        action = dados.get("action")
        # os parâmetros para a função, se existirem
        params = dados.get("params", {})

        # se a ação for resposta direta, retorna o texto diretamente, sem chamar função
        if action == "resposta_direta":
            return params.get("texto", conteudo)

        # se for uma ação de função, procura a função correspondente no mapa e chama com os parâmetros
        funcao = mapa_funcoes.get(action)
        if not funcao:
            return f"Função '{action}' não encontrada."

        # chama a função com os parâmetros extraídos do JSON
        # o **params é pra passar os parâmetros como argumentos nomeados, 
        # por exemplo: funcao(titulo=params['titulo'], prazo=params['prazo'])
        resultado = funcao(**params)

        # se for RAG, a resposta já está formulada
        if action == "buscar_material_rag":
            if resultado.get("ok"):
                return resultado.get("contexto")
            else:
                return resultado.get("mensagem")

        # segunda chamada: LLM formula resposta amigável
        resp_final = client.chat.completions.create(
            model='google/gemma-3-12b-it',
            messages=[
                {"role": "system", "content": "Você é o Jarvis. Formule uma resposta amigável em português com base no resultado. Responda apenas com texto, sem JSON."},
                # passa o resultado da função para o LLM, para que ele possa usar isso como contexto para formular a resposta final
                {"role": "user",   "content": f"Resultado da função {action}: {json.dumps(resultado, ensure_ascii=False)}"}
            ]
        )
        # retorna a resposta final, baseada no resultado da função chamada
        return resp_final.choices[0].message.content

    # se der erro, retorna o conteúdo original (que pode ser uma resposta direta do LLM)
    except json.JSONDecodeError:
        # se não conseguir interpretar como JSON, assume que é uma resposta direta e retorna o texto
        return conteudo
