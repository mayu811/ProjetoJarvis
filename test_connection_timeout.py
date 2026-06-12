# test_connection_timeout.py
import httpx

try:
    with httpx.Client(timeout=10.0) as client:
        resp = client.get('https://llm.liaufms.org/v1/models')
        print(f"Status: {resp.status_code}")
        print("✅ Servidor online")
except Exception as e:
    print(f"❌ Servidor offline: {e}")