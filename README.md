# GenAI-RAG-Platform

## Projektziel

Ziel dieses Projekts ist der Aufbau einer modularen, containerisierten Plattform für **Retrieval-Augmented Generation (RAG)** mithilfe von [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) und einem lokal angebundenen, vollständig **DSGVO-konformen KI-Agenten**. Dieser Agent ist über eine FastAPI-Schnittstelle ansprechbar und als „Custom Skill“ nahtlos in die AnythingLLM-Oberfläche integriert.

Dabei wurden folgende übergeordnete Ziele erreicht und berücksichtigt:

- Entwicklung einer **lokalen, containerisierten RAG-Plattform** auf Basis aktueller Open-Source-Technologien
- **Integration eines intelligenten DSGVO-Assistenten** auf Basis von FastAPI, voll automatisiert per Skill aufrufbar
- **Einbindung von Ollama** für lokale LLM-Berechnungen – bereits erfolgreich lokal gestartet und in AnythingLLM nutzbar
- **REST-API-Funktionalität vollständig bereitgestellt** (Port 3000)
- Erweiterbarkeit der Plattform durch **Custom Skills**, die dynamisch eingebunden und per GUI genutzt werden können
- Fokus auf **Transparenz, Nachvollziehbarkeit und Modularität** – keine Blackbox-Container, sondern nachvollziehbarer Code in eigenen Repos
- vollständige Dokumentation der Setup-Schritte und Design-Entscheidungen

Diese Plattform ist insbesondere darauf ausgelegt, langfristig auf produktionsnahe Infrastrukturen (z. B. **OpenShift**) übertragen werden zu können, wobei volle Kontrolle, Revisionssicherheit und externe GUI-Zugänglichkeit gewährleistet sind. In OpenShift kann die Plattform via Route oder Ingress veröffentlicht werden, sodass die AnythingLLM-Weboberfläche und die REST-API aus internen Netzen oder dem Internet sicher erreichbar sind.

---

## Projektstruktur

```bash
GenAI-RAG-Platform/
├── dsgvo-agent/              # Lokaler FastAPI-Agent zur DSGVO-Auskunft
│   ├── app/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   └── prompts.yaml
│   ├── main.py
│   └── requirements.txt
│
├── anythingllm/             # Manuell geklonter und entkoppelter AnythingLLM-Code
│   ├── server/
│   ├── Dockerfile
│   └── ...
│
├── skills/                  # Custom Skill (z. B. DSGVO-Agent)
│   └── dsgvo-agent.js
│
├── Dockerfile               # Eigener AnythingLLM-Build (inkl. node-fetch)
├── docker-compose.yml       # Docker Start für GUI & API
├── .env                     # Umgebungskonfiguration (leer oder optional)
└── README.md                # Diese Dokumentation
```

---

## Setup

### Tech-Stack

- **AnythingLLM** (neueste stabile Version, lokal kontrolliert)
- **Docker & Docker Compose**
- **FastAPI (Python 3.10)**
- **Node.js + npm** (Skill-Ausführung)
- **Ollama** für lokale LLM-Nutzung – läuft bereits erfolgreich
- **Prisma / SQLite** (intern AnythingLLM)

### Voraussetzungen

- Docker & Compose installiert
- Python ≥ 3.10
- Node.js + npm (falls Skills lokal entwickelt/erweitert werden sollen)

---

## Start der Plattform

### 1. FastAPI DSGVO-Agent starten

```bash
cd dsgvo-agent
uvicorn main:app --reload
```

Läuft dann auf `http://localhost:8000/ask`

✅ Bereits erfolgreich lokal getestet und abrufbar über Postman oder Skill-Call

---

### 2. AnythingLLM mit Custom Skill starten

```bash
cd ..
docker-compose up --build
```

- Web-GUI erreichbar unter: `http://localhost:3001`
- REST-API verfügbar auf: `http://localhost:3000`

✅ Custom Skill DSGVO-Agent wird korrekt geladen, sofern `CUSTOM_SKILLS_DIR` gesetzt ist  
✅ Ollama-Integration wurde über die AnythingLLM-Oberfläche erfolgreich aktiviert

Im späteren OpenShift-Betrieb erfolgt der Zugriff z. B. via Route (`https://anythingllm.apps.internal-domain.de`) – wichtig: offene Ports 3000/3001 oder Reverse Proxy bereitstellen.

---

## Skill: DSGVO-Agent

### Datei: `skills/dsgvo-agent.js`

```js
import fetch from "node-fetch";

export const name = "DSGVO-Agent";
export const description = "Stellt DSGVO-Fragen an den FastAPI-Agenten.";
export const version = "1.0.0";

export async function execute(input) {
  try {
    const response = await fetch("http://host.docker.internal:8000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: input })
    });

    if (!response.ok) {
      return `Fehler beim Aufruf des DSGVO-Agenten: ${response.statusText}`;
    }

    const data = await response.json();
    return data.answer || "Keine Antwort erhalten.";
  } catch (err) {
    return `Fehler: ${err.message}`;
  }
}
```

Der Skill wurde mehrfach getestet und reagiert wie erwartet auf Benutzeranfragen in der GUI.

---

## Wichtige Umgebungsvariablen (docker-compose.yml)

```yaml
environment:
  - NODE_ENV=production
  - STORAGE_DIR=/app/server/storage
  - CUSTOM_SKILLS_DIR=/app/skills
```

```yaml
volumes:
  - ./anythingllm/server/storage:/app/server/storage
  - ./skills:/app/skills
```

Diese Kombination stellt sicher, dass Skills persistent eingebunden und bei jedem Containerstart geladen werden.

---

## Git-Prinzipien & Clean Repo

Das gesamte Projekt wurde auf **sauberen lokalen Strukturen** aufgebaut:

- Fremdrepos werden **niemals im Container** geklont (z. B. AnythingLLM)
- `anythingllm/` ist ein eigener Klon, dessen `.git` entfernt wurde
- eigene Versionierung erfolgt über **ein gemeinsames Git-Repo**

```bash
git init
git add .
git commit -m "Clean setup: DSGVO-Agent & AnythingLLM"
git remote add origin git@github.com:dein-user/dein-repo.git
git push -u origin main
```

---

## Aktueller Stand & Problemstellung (Mai 2025)

Trotz erfolgreichem Start von AnythingLLM (aktuelle Version) und korrekt gemountetem Skill-Verzeichnis wird der DSGVO-Skill **nicht mehr in der GUI angezeigt**. Es wurde bereits sichergestellt, dass:

- `CUSTOM_SKILLS_DIR` gesetzt ist
- `node-fetch` im Container verfügbar ist
- Skill im Format `export const name...` usw. korrekt implementiert ist
- Pfade korrekt gemountet sind und Container-Zugriff möglich ist

Vermutung: 

- keine `loadSkills.js` mehr im Code enthalten
- Skills müssen ggf. über JSON im Verzeichnis `/app/server/storage/plugins/` registriert werden

Nächste Schritte:

- Validierung: Wird überhaupt noch `CUSTOM_SKILLS_DIR` geladen?
- Analyse, ob MCP-basierte Registrierung (plugin.json) erforderlich ist
- Alternativ: Wechsel zurück auf v1.0.34 (funktioniert mit `Custom Tools`)

---

## Fazit & Ausblick

Dieses Projekt bietet nicht nur ein funktionsfähiges lokales Setup mit RAG, Ollama und DSGVO-Skill – es dokumentiert auch sämtliche Schritte hin zu einer nachvollziehbaren und kontrollierten LLM-Plattform. Die wichtigsten Meilensteine wurden erreicht:

✅ AnythingLLM läuft lokal & steuerbar mit GUI  
✅ Ollama ist eingebunden und lokal verwendbar  
✅ DSGVO-Agent wurde in Python entwickelt und über Skill sauber integriert  
✅ Logging, Build-Prozess und Skill-Verwaltung nachvollziehbar eingerichtet

Zukünftige Schritte:
- MCP/Plugin-basierte Skill-Registrierung ausloten
- **Bereitstellung der Plattform in OpenShift**, inkl. externem Zugriff auf Web GUI & API über sichere Endpunkte
- AI Agent füttern und weiterentwickeln, sodass er Data Governance Abfragen besser beantworten kann

> Ziel ist es, eine **rechtskonforme, auditierbare und modulare LLM-Infrastruktur** zu schaffen, die für reale Enterprise-Setups vorbereitet ist.
