# test_qwen.py
import httpx
from openai import OpenAI
# Cliente que segue redirecionamentos
http_client = httpx.Client(
    verify=False,
    follow_redirects=True,  # ← importante!
    timeout=60.0
)
client = OpenAI(
    #base_url='https://llm.liaufms.org/v1/qwen2-5-14b-instruct-awq',
    base_url='https://llm.liaufms.org/v1',
    api_key='REIkURcI7rTTqsTwlJi8MrgnKFw0iqky7EzhH-l-k'
    , http_client=http_client
)
try:
    print("Testando Qwen com redirect seguido...")
    resp = client.chat.completions.create(
        model='Qwen/Qwen2.5-14B-Instruct-AWQ',
        messages=[{"role": "user", "content": "Hi"}],
        max_tokens=20,
        temperature=0.7
    )
    print(f"✅ Sucesso! Resposta: {resp.choices[0].message.content}")
except Exception as e:
    print(f"❌ Erro: {e}")