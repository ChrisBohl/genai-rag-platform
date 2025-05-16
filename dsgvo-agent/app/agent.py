import requests
import yaml

def load_policies(path="app/prompts.yaml"):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def ask_ollama(prompt: str, model="mistral"):
    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]

def run_agent(user_input: str):
    policies = load_policies()
    full_prompt = f"""
Du bist ein KI-Agent für DSGVO-Daten-Governance.
Hier die Regeln:
{policies['richtlinien']}

Frage:
{user_input}

Antwort bitte mit: Entscheidung + Begründung + Empfehlung.
"""
    return ask_ollama(full_prompt)
