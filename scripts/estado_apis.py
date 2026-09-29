import os, requests
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("ESTADO DE APIs IA")
print("=" * 60)

# Groq
groq_key = os.getenv("GROQ_API_KEY", "")
if groq_key:
    try:
        r = requests.get(
            "https://api.groq.com/openai/v1/models",
            headers={"Authorization": f"Bearer {groq_key}"},
            timeout=10,
        )
        if r.status_code == 200:
            models = [m["id"] for m in r.json().get("data", [])]
            print(f"Groq: OK ({len(models)} modelos)")
            # Verificar modelos utiles
            utiles = [m for m in models if any(k in m.lower() for k in ["llama", "qwen", "mixtral"])]
            print(f"  Modelos utiles: {len(utiles)}")
        else:
            print(f"Groq: HTTP {r.status_code}")
    except Exception as e:
        print(f"Groq: ERROR {e}")
else:
    print("Groq: Sin key")

# OpenRouter
or_key = os.getenv("OPENROUTER_API_KEY", "")
if or_key:
    try:
        r = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {or_key}"},
            timeout=10,
        )
        if r.status_code == 200:
            data = r.json().get("data", {})
            print(f"OpenRouter: OK")
            print(f"  Creditos: {data.get('limit', '?')} - usado: {data.get('usage', '?')}")
            print(f"  Free tier: {data.get('is_free_tier', '?')}")
        else:
            print(f"OpenRouter: HTTP {r.status_code} - {r.text[:100]}")
    except Exception as e:
        print(f"OpenRouter: ERROR {e}")
else:
    print("OpenRouter: Sin key")

# Gemini
gem_key = os.getenv("GEMINI_API_KEY", "")
if gem_key:
    try:
        r = requests.get(
            f"https://generativelanguage.googleapis.com/v1/models?key={gem_key}",
            timeout=10,
        )
        if r.status_code == 200:
            print(f"Gemini: OK ({len(r.json().get('models', []))} modelos)")
        else:
            print(f"Gemini: HTTP {r.status_code}")
    except Exception as e:
        print(f"Gemini: ERROR {e}")
else:
    print("Gemini: Sin key")

print("=" * 60)
