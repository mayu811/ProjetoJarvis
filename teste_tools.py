from openai import OpenAI

client = OpenAI(
    base_url='https://llm.liaufms.org/v1/gemma-3-12b-it',
    api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A'
)

TOOL_TESTE = [
    {
        "type": "function",
        "function": {
            "name": "adicionar_tarefa",
            "description": "Adiciona uma tarefa.",
            "parameters": {
                "type": "object",
                "properties": {
                    "titulo": {"type": "string"}
                },
                "required": ["titulo"]
            }
        }
    }
]

resp = client.chat.completions.create(
    model='google/gemma-3-12b-it',
    messages=[{'role': 'user', 'content': 'Adiciona uma tarefa chamada estudar matemática'}],
    tools=TOOL_TESTE,
    tool_choice="auto"
)

print(resp.choices[0].message)