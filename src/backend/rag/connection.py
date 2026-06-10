'''
#cliente para acessar a API do LLM (configurado para usar o modelo Gemma-3.12b-it hospedado no LIA)
'''

from openai import OpenAI

client = OpenAI(
    base_url='https://llm.liaufms.org/v1/gemma-3-12b-it',
    api_key='Cxt2ftLF7d3mHS2JdiFqB-eSDAQeZvFATPXPs02lV9A'
)