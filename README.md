# GenAI-RAG-Platform

Dieses Repository vereint einen modular aufgebauten GenAI-Technologie-Stack mit Schwerpunkt auf datenschutzkonformer Nutzung in Unternehmenskontexten. Es integriert:

- **AnythingLLM (neueste Version)** als RAG-Plattform mit GUI und Vektorunterstützung
- Einen **DSGVO-konformen FastAPI-Agenten**, der als Custom Skill über die AnythingLLM-GUI eingebunden ist
- Eine **klare Trennung von Backend, Skills und Datenhaltung** in einem Docker-basierten Setup

---

## Projektstruktur

```text
GenAI-RAG-Platform/
│
├── dsgvo-agent/              # FastAPI-basierter DSGVO-Agent
│   ├── app/                  # API-Logik
│   ├── main.py               # Entry Point
│   └── requirements.txt      # Python-Abhängigkeiten
│
├── rag-anythingllm/          # Offizielle AnythingLLM-Installation (Cloned Codebase)
│
├── skills/                   # Enthält eigene Skills (z. B. DSGVO-Agent)
│   └── dsgvo-agent.js        # Der Skill als .js/.mjs Datei
│
├── Dockerfile                # Custom Build für AnythingLLM mit node-fetch
├── docker-compose.yml        # Orchestrierung von AnythingLLM mit Mounts
└── .env                      # Umgebungsvariablen (derzeit leer)
```

---

## Setup

### Voraussetzungen

- Docker & Docker Compose
- Python 3.11+ mit `uvicorn`, `fastapi`, `pydantic`
- Node.js **muss lokal nicht installiert** sein – es wird im Container bereitgestellt.

---

### Start der Anwendung

#### 1. DSGVO-Agent (FastAPI)

```bash
cd dsgvo-agent
uvicorn main:app --reload
```

Der Agent läuft anschließend auf:  
`http://localhost:8000/ask` (POST)

---

#### 2. AnythingLLM inkl. Skill-Unterstützung

```bash
cd ..
docker-compose up --build
```

Anschließend erreichbar über:

- **Web GUI**: [http://localhost:3001](http://localhost:3001)
- **REST API (optional)**: [http://localhost:3000](http://localhost:3000)

---

## Skill-Integration: DSGVO-Agent

Der Skill wird automatisch beim Start des Containers aus dem Verzeichnis `./skills` geladen.

### Skill-Details (`skills/dsgvo-agent.js`)

- Ruft lokal laufenden FastAPI-Agenten via `fetch` auf
- Wird als "DSGVO-Agent" in der GUI angezeigt
- Kommuniziert über `http://host.docker.internal:8000/ask`

**Voraussetzung:**  
Die Umgebungsvariable `CUSTOM_SKILLS_DIR` ist im Compose-File korrekt gesetzt und das Volume wird gemountet.

---

## Hinweise zur Docker-Nutzung

Das AnythingLLM-Image wurde **custom gebaut** (siehe Dockerfile), da `node-fetch` nicht standardmäßig enthalten ist.  
Achte darauf, dass du bei Änderungen am Skill auch `docker-compose up --build` ausführst, damit Änderungen übernommen werden.

---

## Weiterentwicklung

- Migration auf AnythingLLM MCP-Plugins (optional, sobald stabil dokumentiert)
- Skill-Registrierung per JSON (z. B. `/app/server/storage/plugins/`)
- Monitoring & Logging für Produktionsbetrieb
- Authentifizierung der DSGVO-API

---

## Git-Konventionen

- Dieses Repo ist **Quelle der Wahrheit**
- Keine direkten Clones von Fremd-Repos in Container → immer per `git clone` in eigenen Unterordner
- Eigene Skills, Images und APIs gehören **immer versioniert** ins Repo

---

## Lizenz / Nutzung

Dieses Projekt befindet sich in Entwicklung. Bei produktiver Nutzung bitte Datenschutz und interne Vorgaben beachten.