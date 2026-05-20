#chama a API do LLM para obter respostas
from datetime import datetime
import json
from openai import OpenAI
from src.backend.tools.definitions import (
    TOOLS,
    adicionar_tarefa,
    listar_tarefas,
    concluir_tarefa,
    adicionar_compromisso,
    consultar_agenda,
    buscar_material_rag
)

client = OpenAI(
    base_url='https://llm.liaufms.org/v1/gemma-3-12b-it',
    api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A'
)

data_atual = datetime.now().strftime("%d/%m/%Y")
hora_atual = datetime.now().strftime("%H:%M")

#print("LLM client pronto!")

# sistema de prompt para o LLM entender como usar as funções
SYSTEM_PROMPT = f"""
Você é o Jarvis, um assistente acadêmico inteligente.
Hoje é dia {data_atual} e são {hora_atual}.

Quando o usuário pedir algo, responda SEMPRE em JSON com este formato:

Para chamar uma função:
{{"action": "nome_da_funcao", "params": {{"param1": "valor1"}}}}

Para responder diretamente:
{{"action": "resposta_direta", "params": {{"texto": "sua resposta aqui"}}}}

Para múltiplas ações:
{{"actions": [
    {{"action": "concluir_tarefa", "params": {{"titulo": "tarefa1"}}}},
    {{"action": "concluir_tarefa", "params": {{"titulo": "tarefa2"}}}}
]}}

Funções disponíveis:
- adicionar_tarefa(titulo, prazo, prioridade): adiciona uma tarefa
- listar_tarefas(): lista tarefas pendentes
- concluir_tarefa(titulo): marca tarefa como concluída
- consultar_agenda(data): consulta compromissos na agenda
- adicionar_compromisso(titulo, data_hora, descricao, local): adiciona compromisso ou evento
- buscar_material_rag(pergunta): busca informaçõesnos documentos enviados

Responda APENAS com o JSON, sem texto adicional.
"""

mapa_funcoes = {
    "adicionar_tarefa":    adicionar_tarefa,
    "listar_tarefas":      listar_tarefas,
    "concluir_tarefa":     concluir_tarefa,
    "consultar_agenda":    consultar_agenda,
    "buscar_material_rag": buscar_material_rag,
    "adicionar_compromisso":  adicionar_compromisso,
    #"marcar_compromisso": marcar_compromisso
}

def processar_mensagem(mensagem: str) -> str:

    resp = client.chat.completions.create(
        model='google/gemma-3-12b-it',
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": mensagem}
        ]
    )

    conteudo = resp.choices[0].message.content.strip()

    try:
        # remove blocos ```json ... ``` se existirem
        if conteudo.startswith("```"):
            conteudo = conteudo.split("```")[1]
            if conteudo.startswith("json"):
                conteudo = conteudo[4:]

        dados = json.loads(conteudo)
        action = dados.get("action")
        params = dados.get("params", {})

        if action == "resposta_direta":
            return params.get("texto", conteudo)

        funcao = mapa_funcoes.get(action)
        if not funcao:
            return f"Função '{action}' não encontrada."

        resultado = funcao(**params)

        # segunda chamada: LLM formula resposta amigável
        resp_final = client.chat.completions.create(
            model='google/gemma-3-12b-it',
            messages=[
                {"role": "system", "content": "Você é o Jarvis. Formule uma resposta amigável em português com base no resultado. Responda apenas com texto, sem JSON."},
                {"role": "user",   "content": f"Resultado da função {action}: {json.dumps(resultado, ensure_ascii=False)}"}
            ]
        )
        return resp_final.choices[0].message.content

    except json.JSONDecodeError:
        return conteudo
    


def processar_mensagem(mensagem: str) -> str:
    historico = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": mensagem}
    ]

    MAX_TURNOS = 5

    for turno in range(MAX_TURNOS):
        resp = client.chat.completions.create(
            model='google/gemma-3-12b-it',
            messages=historico
        )

        conteudo = resp.choices[0].message.content.strip()
        print(f"\n=== TURNO {turno + 1} ===")
        print(f"LLM retornou: {conteudo}")

        if conteudo.startswith("```"):
            conteudo = conteudo.split("```")[1]
            if conteudo.startswith("json"):
                conteudo = conteudo[4:]

        try:
            dados = json.loads(conteudo)

            # normaliza para sempre usar lista de actions
            if "action" in dados and "actions" not in dados:
                actions = [{"action": dados["action"], "params": dados.get("params", {})}]
            else:
                actions = dados.get("actions", [])

            # resposta direta — encerra o loop
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
                resultados.append({"action": action, "resultado": resultado})

            historico.append({"role": "assistant", "content": conteudo})
            historico.append({
                "role": "user",
                "content": f"Resultados: {json.dumps(resultados, ensure_ascii=False)}. Continue ou responda ao usuário em JSON."
            })

        except json.JSONDecodeError:
            return conteudo

    return "Não consegui completar a operação."
