'''
 Área de acesso a API do LLM
'''
import httpx
from openai import OpenAI

http_client = httpx.Client(verify=False)

MODEL_NAME = 'Qwen/Qwen2.5-14B-Instruct-AWQ'
API_KEY = 'REIkURcI7rTTqsTwlJi8MrgnKFwOiqky7Ezh7hH-l-k'

# Configuração para Qwen2.5-14B
client = OpenAI(
    base_url='https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq',
    api_key=API_KEY,
    http_client=http_client
)

