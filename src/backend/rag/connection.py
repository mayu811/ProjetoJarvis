'''
#cliente para acessar a API do LLM (configurado para usar o modelo Gemma-3.12b-it hospedado no LIA)
'''
# src/backend/rag/connection.py
import httpx
from openai import OpenAI

http_client = httpx.Client(verify=False)

# Configuração para Qwen2.5-14B
client = OpenAI(
    base_url='https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq',
    api_key='REIKURC17rTTqsTwLJi8MrgnKFw0iqky7Ezh7hH-L-k',
    http_client=http_client
)

# Opcional: manter compatibilidade com o modelo antigo se precisar alternar
# MODEL_NAME = 'Qwen/Qwen2.5-14B-Instruct-AWQ'
MODEL_NAME = 'Qwen/Qwen2.5-14B-Instruct-AWQ'