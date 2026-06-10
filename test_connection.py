# test_connection.py
import requests
import httpx

# Teste básico com requests
try:
    response = requests.get('https://llm.liaufms.org', verify=False, timeout=10)
    print(f"Status code: {response.status_code}")
    print(f"Servidor respondeu: {response.status_code == 200}")
except Exception as e:
    print(f"Erro no requests: {e}")

# Teste com httpx
try:
    with httpx.Client(verify=False, timeout=10) as client:
        resp = client.get('https://llm.liaufms.org')
        print(f"HTTPS: Status {resp.status_code}")
except Exception as e:
    print(f"Erro no httpx: {e}")

# Teste do endpoint da API
try:
    with httpx.Client(verify=False, timeout=10) as client:
        resp = client.get('https://llm.liaufms.org/v1/models')
        print(f"API models: {resp.status_code}")
        if resp.status_code == 200:
            print(f"Modelos disponíveis: {resp.json()}")
except Exception as e:
    print(f"Erro na API: {e}")