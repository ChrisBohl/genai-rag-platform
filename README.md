# GenAI-RAG-Platform

## Projektziel

Ziel dieses Projekts ist der Aufbau einer modularen, containerisierten Plattform für **Retrieval-Augmented Generation (RAG)** mithilfe von [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) und einem lokalen **DSGVO-konformen KI-Agenten**, der über eine FastAPI-Schnittstelle angesprochen wird. 

Die Plattform verfolgt insbesondere folgende Ziele:

- Bereitstellung einer benutzerfreundlichen Web-Oberfläche (AnythingLLM) für kontextbasierte LLM-Interaktionen
- Integration eines lokalen DSGVO-Agents als ausführbare „Custom Skill“ innerhalb von AnythingLLM
- Einhaltung der Datenschutzgrundverordnung (DSGVO) durch lokale Verarbeitung, Trennung von Verantwortlichkeiten und keine externe Datenübertragung
- Modularität und Erweiterbarkeit durch Docker, Custom Skills und einen sauberen Codeaufbau
- Bereitstellung einer sauberen Codebasis und Dokumentation für künftige Entwickler oder Auditoren

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
├── skills/                   # Custom Skill für AnythingLLM
│   └── dsgvo-agent.js
│
├── Dockerfile                # Dockerfile für eigenen AnythingLLM-Build (inkl. node-fetch)
├── docker-compose.yml        # Startet LLM-GUI & bindet DSGVO-Agent ein
├── .env                      # Umgebungskonfiguration (leer oder optional)
└── README.md                 # Diese Dokumentation
```

---

## Setup

### Tech-Stack

- AnythingLLM (aktuelle Version, lokal gebautes Image)
- Docker & Docker Compose
- FastAPI (Python 3.10)
- Node.js / JavaScript (Custom Skill)
- Ollama (optional, lokale LLM-Anbindung)
- Prisma / SQLite (intern AnythingLLM)

---

## Setup-Anleitung
### Voraussetzungen
- Docker & Docker Compose installiert
- Python ≥ 3.10 installiert (für DSGVO-Agent)
- Node.js & npm (für Skill-Entwicklung, falls lokal)

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