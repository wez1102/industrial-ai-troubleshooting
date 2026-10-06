# Industrial AI Troubleshooting & Maintenance Assistant — Python Edition

> **Project type:** Python / FastAPI / RAG / Local LLM (Ollama) / PostgreSQL + pgvector / CI/CD
> **Primary goal:** Build a production-style AI application *and the pipelines around it* — data ingestion, RAG, evaluation, CI, and CD — the way a professional team would, with **$0 required spend**.

---

## 0. What Changed from the Java Version

This document is a Python port of the original Java/Spring Boot requirements, with one major addition: **CI/CD and pipeline engineering are now a first-class goal**, not a Phase 7 afterthought. The pipeline is built on day one and grows with every feature.

### Java → Python mapping

| Concern | Java version | Python version |
|---|---|---|
| Language / runtime | Java 21 | Python 3.12+ (test on 3.12 and 3.13) |
| Web framework | Spring Boot (Web) | **FastAPI** + Uvicorn |
| Validation / DTOs | Bean Validation, records | **Pydantic v2** models |
| Configuration | `application.yml`, profiles | **pydantic-settings** (env vars + `.env`) |
| Dependency injection | Spring constructor injection | FastAPI `Depends` + explicit constructors |
| ORM / persistence | Spring Data JPA | **SQLAlchemy 2.0** (async) + **psycopg 3** |
| Migrations | Flyway | **Alembic** |
| Vector search | pgvector | pgvector + `pgvector` Python package |
| LLM framework | LangChain4j | Explicit RAG code + official **`ollama`** client (LangChain optional, see §8.2) |
| Embeddings | LangChain4j ONNX model | **fastembed** (ONNX, CPU, no PyTorch) |
| Structured output | LangChain4j AI Services | Ollama JSON-schema output + **Pydantic** validation |
| Health checks | Actuator | Custom `/health/live` and `/health/ready` endpoints |
| API docs | springdoc / Swagger | Built into FastAPI (`/docs`, `/openapi.json`) |
| Error handling | `@ControllerAdvice` | FastAPI exception handlers |
| Build tool | Maven Wrapper | **uv** (lockfile: `uv.lock`) + `Makefile` |
| Unit tests | JUnit 5 + Mockito | **pytest** + `unittest.mock` / pytest fixtures |
| Integration tests | Testcontainers (Java) | **testcontainers-python** |
| HTTP tests | MockMvc / REST Assured | `httpx.AsyncClient` against the ASGI app |
| Lint / format | Checkstyle / Spotless | **ruff** (lint + format) |
| Static types | javac | **mypy** (strict on `src/`) |
| Logging | SLF4J / Logback | **structlog** (JSON logs) |
| CLI | — | **Typer** (`plantassist ingest`, `plantassist eval`) |

---

## 1. Project Summary

Build an AI-powered troubleshooting assistant for industrial equipment.

A technician or engineer enters a machine fault, alarm, symptom, or maintenance question, such as:

> **"Servo axis 4 has a following error after the machine accelerates. What should I check?"**

The application will:

1. Search machine manuals, SOPs, troubleshooting guides, and prior incident records.
2. Retrieve the most relevant document sections using semantic search.
3. Send the retrieved context to a locally running LLM.
4. Generate a structured troubleshooting response.
5. Cite the source documents used.
6. Optionally call safe, read-only diagnostic tools that return mock machine status.
7. Store the incident, retrieved evidence, response, and resolution.
8. Evaluate whether retrieval and generated answers are actually good.

Around the application, the project builds **five pipelines**:

| Pipeline | What it does | Where it runs |
|---|---|---|
| **Data ingestion pipeline** | Parse → validate → chunk → embed → store documents, idempotently | CLI / API / CI |
| **RAG inference pipeline** | Question → embed → retrieve → prompt → LLM → validate → respond | Application runtime |
| **Evaluation pipeline** | Measure retrieval and answer quality against a ground-truth set | CI (retrieval) + nightly/manual (LLM) |
| **CI pipeline** | Lint, type-check, test, scan, build, smoke-test, gate on quality | GitHub Actions on every PR |
| **CD / release pipeline** | Version, build, sign, publish, deploy, verify | GitHub Actions on merge/release |

The project is intended to look like a **real backend AI system owned by a real team**, not a chatbot demo.

---

## 2. Cost Constraint

### Mandatory requirement

**The project must be possible to build, test, release, and run without paying for APIs, cloud hosting, databases, CI, or AI models.**

### Free/local stack

| Component | Choice | Cost |
|---|---|---:|
| Language | Python 3.12+ | $0 |
| Package/env manager | uv | $0 |
| API framework | FastAPI + Uvicorn | $0 |
| Local LLM runtime | Ollama | $0 |
| Chat model | Small open-weight instruct model via Ollama | $0 |
| Embeddings | fastembed (local ONNX) | $0 |
| Database | PostgreSQL + pgvector (Docker) | $0 |
| Containers | Docker / Docker Compose | $0 |
| Testing | pytest, testcontainers-python, Hypothesis | $0 |
| CI/CD | GitHub Actions — free on public repositories (standard runners and self-hosted runners) | $0 |
| Container registry | GitHub Container Registry (GHCR), public images | $0 |
| Security scanning | pip-audit, Bandit, gitleaks, Trivy, CodeQL, Dependabot | $0 |
| Supply chain | Syft (SBOM), Cosign keyless signing (Sigstore) | $0 |
| Docs site / reports | GitHub Pages (public repo) | $0 |
| Hosting | Local Docker / your own machine | $0 |

### Important notes

- No OpenAI, Anthropic, Pinecone, paid hosted PostgreSQL, or paid cloud deployment is required.
- **Keep the repository public.** GitHub Actions minutes are free for public repositories; private repositories have a limited monthly allowance and self-hosted runner usage in private repos can be billable. Check GitHub's current Actions billing docs before relying on any free tier.
- Use only **standard** GitHub-hosted runners. Larger runners are billed even on public repos.

---

## 3. Why This Project Exists

This project should prove that the developer can build:

- Python backend services with clean architecture
- REST APIs with validation and consistent error handling
- Relational persistence with migrations
- LLM applications and Retrieval-Augmented Generation (RAG)
- Vector search
- Tool/function calling
- Structured, validated AI outputs
- **Data pipelines** (idempotent, versioned ingestion)
- **ML evaluation pipelines** with regression gates
- **CI pipelines** with quality, security, and AI-quality gates
- **CD pipelines** with versioning, signed artifacts, environments, and approvals
- Dockerized services, observability, and production-minded failure handling

Target roles:

- AI Engineer / Applied AI Engineer
- Machine Learning Engineer / MLOps Engineer
- Backend Software Engineer (Python)
- Platform / DevOps-leaning Software Engineer
- Industrial AI / automation software roles

---

## 4. Project Name

Working name: **`PlantAssist AI`**

Recommended repository name:

```text
industrial-ai-troubleshooting
```

Python package name: `plantassist`

---

## 5. Core Use Case

### Example input

```text
Machine: Case Packer 01
Alarm:   Servo Axis 4 Following Error
Symptoms:
  The fault occurs during rapid acceleration.
  Motor temperature appears normal.
  The issue started after maintenance.
```

### Example output

```json
{
  "severity": "HIGH",
  "summary": "The following error may be caused by a mechanical restriction, encoder issue, incorrect tuning, or a post-maintenance alignment problem.",
  "possibleCauses": [
    { "cause": "Mechanical binding or increased axis load", "confidence": 0.82 },
    { "cause": "Encoder or feedback connection issue", "confidence": 0.74 }
  ],
  "recommendedChecks": [
    { "step": 1, "action": "Verify the axis can move freely with power isolated.", "safetyCritical": true },
    { "step": 2, "action": "Inspect encoder and motor feedback connectors.", "safetyCritical": false }
  ],
  "sources": [
    { "document": "servo_troubleshooting_manual.md", "section": "Following Error", "chunkId": "servo-manual-v1:following-error:002" }
  ],
  "insufficientEvidence": false,
  "disclaimer": "AI-generated guidance. Does not replace qualified personnel or site lockout/tagout procedures."
}
```

The schema may evolve, but responses must remain structured, machine-readable, and versioned.

> API JSON uses camelCase; Python code uses snake_case. Configure Pydantic with an alias generator (`alias_generator=to_camel`, `populate_by_name=True`) so both sides stay idiomatic.

---

## 6. Safety Boundary

This is an **educational portfolio project**, not a certified industrial safety system.

The application must:

- Clearly state that AI recommendations do not replace qualified personnel.
- Never claim that a machine is safe to energize.
- Never operate real equipment.
- Keep all tool calls read-only and backed by mock data.
- Label safety-critical recommendations.
- Prefer source-grounded answers over unsupported guesses.
- Return `insufficientEvidence: true` when documents do not support an answer.

No proprietary employer documents, customer documents, machine programs, credentials, or private plant data may be committed. Use synthetic or openly licensed material only. The CI pipeline enforces part of this with secret scanning (§23.4).

---

## 7. High-Level Architecture

### 7.1 Runtime architecture

```text
                        ┌──────────────────────┐
                        │      Web Client      │
                        │  Minimal HTML/JS UI  │
                        └──────────┬───────────┘
                                   │ REST (JSON)
                  ┌────────────────▼────────────────┐
                  │        FastAPI application       │
                  │  routers → services → adapters   │
                  └────────────────┬────────────────┘
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
┌──────────────────┐     ┌──────────────────┐      ┌───────────────────┐
│ Troubleshooting  │     │  RAG / Retrieval │      │ Incident Service  │
│ Orchestrator     │     │  Service         │      │                   │
└────────┬─────────┘     └────────┬─────────┘      └─────────┬─────────┘
         │                        │                          │
         ▼                        ▼                          ▼
┌──────────────────┐     ┌──────────────────┐      ┌───────────────────┐
│  LLM adapter     │     │ fastembed (ONNX) │      │ PostgreSQL        │
│  (Ollama / Fake) │     │ local embeddings │      │ + pgvector        │
└────────┬─────────┘     └──────────────────┘      └───────────────────┘
         ▼
┌──────────────────┐
│ Ollama (host or  │
│ container)       │
└──────────────────┘
```

### 7.2 Delivery architecture (the pipelines around the code)

```text
 Developer laptop                     GitHub                                  Targets
┌──────────────────┐   push/PR   ┌──────────────────────────────┐
│ pre-commit hooks │ ──────────► │ CI workflow (every PR)       │
│ make lint/test   │             │  lint · types · tests ·      │
└──────────────────┘             │  security · build · smoke ·  │
                                 │  retrieval-eval gate         │
                                 └──────────────┬───────────────┘
                                                │ merge to main
                                 ┌──────────────▼───────────────┐
                                 │ Release workflow             │
                                 │  version · changelog ·       │      ┌──────────────┐
                                 │  build · SBOM · sign · push ─┼────► │ GHCR image   │
                                 └──────────────┬───────────────┘      └──────┬───────┘
                                                │                             │ pull
                                 ┌──────────────▼───────────────┐      ┌──────▼───────┐
                                 │ Deploy workflow              │      │ staging      │
                                 │  staging → (approval) → prod ├────► │ (ephemeral)  │
                                 └──────────────────────────────┘      ├──────────────┤
                                 ┌──────────────────────────────┐      │ production   │
                                 │ Nightly LLM-eval workflow    │      │ (your own    │
                                 │  answer quality · schema     │      │  machine)    │
                                 │  validity · report → Pages   │      └──────────────┘
                                 └──────────────────────────────┘
```

---

## 8. Technology Stack

### 8.1 Backend

- Python 3.12+ (CI matrix: 3.12 and 3.13)
- uv for dependency management, virtualenvs, and the lockfile
- FastAPI + Uvicorn
- Pydantic v2 + pydantic-settings
- SQLAlchemy 2.0 (async) + psycopg 3
- Alembic for migrations
- Typer for the CLI
- structlog for JSON logging
- asgi-correlation-id (or a small middleware) for request IDs

### 8.2 AI

- **Ollama** for local LLM inference via the official `ollama` Python client (async)
- **fastembed** for local embeddings (default model: `BAAI/bge-small-en-v1.5`, 384 dimensions)
- Structured output: pass the Pydantic JSON schema to Ollama's `format` parameter, then validate with Pydantic
- Tool calling: Ollama's native `tools` support with an explicit tool-execution loop

**Framework decision (record as ADR-001):** Implement the RAG pipeline with explicit code — parser, chunker, embedder, retriever, context builder, prompt factory — rather than hiding it behind LangChain or LlamaIndex. This is more educational and easier to test. A LangChain adapter can be added later as a stretch goal if the resume needs the keyword; the adapter interface (§15) makes that a small change.

### 8.3 Database

- PostgreSQL 16+ with the pgvector extension (`pgvector/pgvector` Docker image)
- Alembic migrations (including `CREATE EXTENSION IF NOT EXISTS vector`)
- HNSW index on the embedding column once data volume justifies it

### 8.4 Testing

- pytest, pytest-asyncio, pytest-cov
- testcontainers-python (PostgreSQL + pgvector)
- httpx `AsyncClient` with `ASGITransport` for API tests
- respx for mocking Ollama HTTP calls
- Hypothesis for property-based tests of the chunker
- A deterministic **FakeLLM** adapter for end-to-end tests without Ollama

### 8.5 Code quality

- ruff (lint + format, including security rules `S`)
- mypy (strict for `src/`)
- import-linter (enforces the layered architecture in CI)
- pre-commit (runs the fast checks before every commit)

### 8.6 CI/CD and supply chain

- GitHub Actions (workflows, reusable workflows, composite actions, environments)
- Docker Buildx with GitHub Actions cache
- GHCR for images
- release-please (automated versioning + CHANGELOG from Conventional Commits)
- Dependabot (Python dependencies, GitHub Actions, Docker base images)
- pip-audit, Bandit, gitleaks, Trivy, CodeQL
- Syft (SBOM) and Cosign (keyless signing)

### 8.7 Optional UI

Minimal HTML + CSS + vanilla JS served by FastAPI's `StaticFiles`. A React frontend is not required.

---

## 9. Local Development Requirements

### Required software

| Tool | Purpose |
|---|---|
| Python 3.12+ | Runtime (uv can install it for you: `uv python install 3.12`) |
| uv | Dependencies, virtualenv, lockfile, running tools |
| Docker + Docker Compose | PostgreSQL/pgvector, integration tests, app image |
| Ollama | Local LLM inference at `http://localhost:11434` |
| Git | Source control |
| make | Task runner (on Windows: use WSL2, or swap `Makefile` for `just`) |
| GitHub CLI (`gh`) | Optional, handy for PRs and workflow runs |

### One-command developer experience

Every task a developer or CI runs must be a `make` target. **CI calls the same targets** — this is the "CI parity" principle (§22.1).

```bash
make install            # uv sync --frozen + pre-commit install
make up                 # docker compose up -d --wait (postgres)
make migrate            # alembic upgrade head
make ingest             # plantassist ingest sample-data/manuals
make run                # uvicorn plantassist.main:app --reload
make lint               # ruff check + ruff format --check + import-linter
make typecheck          # mypy src
make test-unit          # pytest -m unit --cov
make test-integration   # pytest -m integration (Testcontainers)
make test-e2e           # pytest -m e2e (FakeLLM, full stack)
make test-ai            # pytest -m ai (real Ollama — slow)
make eval-retrieval     # retrieval metrics + regression gate
make eval-llm           # answer-quality evaluation (needs Ollama)
make security           # pip-audit + bandit + gitleaks
make image              # docker build
make smoke              # start the built image + hit health endpoints
make ci                 # everything CI runs, locally
```

### Model configuration

The LLM model must be configurable, never hard-coded:

```env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=<local-model-name>
LLM_PROVIDER=ollama        # ollama | fake
```

Pick a small instruct model that supports tool calling and JSON output from the Ollama library (roughly the 1–4B parameter range for CPU-only machines). Use an even smaller model for CI evaluation runs.

---

## 10. Practical Hardware Target

| | Minimum practical | Preferred |
|---|---|---|
| RAM | 8 GB | 16 GB+ |
| CPU | Modern multi-core | Modern multi-core |
| GPU | Not required | Use if available |
| Disk | Several GB free | 20 GB+ (images, models) |

The model must be chosen so the application can be demonstrated on CPU hardware. If a model is too slow, use a smaller one. Note: GitHub's standard Linux runners are CPU-only, which shapes the CI evaluation strategy (§24).

---

## 11. Functional Requirements

### FR-01 — Document ingestion

The system shall ingest troubleshooting documents.

- Initial formats: Markdown, TXT
- Later: PDF (via `pypdf`)

Each document stores: document ID, filename, document type, equipment type, version, **content hash (SHA-256)**, ingestion timestamp. Each chunk stores: chunk text, metadata, embedding.

Documents carry YAML front matter so metadata is explicit and validatable:

```markdown
---
document_id: servo-manual-v1
title: Servo Troubleshooting Manual
equipment_type: servo_drive
version: 1.0.0
license: synthetic
---
# Following Error
...
```

### FR-02 — Ingestion is an idempotent, versioned pipeline

Ingestion must behave like a professional data pipeline:

1. **Discover** files in the source directory.
2. **Validate** front matter against a Pydantic schema; reject empty or unsupported files.
3. **Hash** content; skip documents whose hash is unchanged (idempotency).
4. **Parse** into sections (Markdown headings).
5. **Chunk** with configurable size and overlap.
6. **Embed** in batches.
7. **Upsert** inside a single transaction per document (old chunks replaced atomically).
8. **Report** counts: discovered, skipped, ingested, failed, chunks written, duration.

Running ingestion twice on the same corpus must produce zero changes the second time.

### FR-03 — Deterministic chunk IDs

Chunk IDs must be stable across re-ingestion so the evaluation ground truth does not break:

```text
{document_id}:{section_slug}:{chunk_index:03d}
e.g. servo-manual-v1:following-error:002
```

### FR-04 — Chunking

Chunks retain metadata:

```json
{
  "documentId": "servo-manual-v1",
  "documentName": "Servo Troubleshooting Manual",
  "section": "Following Error",
  "equipmentType": "servo_drive",
  "chunkIndex": 2
}
```

Chunk size, overlap, and splitting strategy must be configurable (`RAG_CHUNK_SIZE`, `RAG_CHUNK_OVERLAP`).

### FR-05 — Local embeddings

Embeddings are generated locally with fastembed. The embedding model name and dimension are configuration; the application must **fail fast at startup** if the configured dimension does not match the pgvector column.

### FR-06 — Vector storage and similarity search

Embeddings are stored in PostgreSQL using pgvector, queried with cosine distance.

```env
RAG_TOP_K=5
RAG_MIN_SCORE=0.70
```

Thresholds are chosen experimentally using the evaluation pipeline, not guessed.

### FR-07 — Semantic retrieval

Given a query, return the top-K chunks with similarity score, source document, section, and chunk ID. Retrieval must be usable independently of the LLM (`POST /api/v1/search`).

### FR-08 — Retrieval-Augmented Generation

Retrieved chunks are passed to the LLM. The prompt must instruct the model to:

1. Use only the supplied evidence.
2. Avoid inventing machine details.
3. Cite retrieved chunk IDs.
4. Indicate when evidence is insufficient.
5. Return output matching the JSON schema.

### FR-09 — Structured AI output

The LLM response maps to a Pydantic model:

```python
class TroubleshootingResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    severity: Severity
    summary: str
    possible_causes: list[PossibleCause]
    recommended_checks: list[TroubleshootingStep]
    sources: list[SourceCitation]
    insufficient_evidence: bool
```

Invalid model output must be handled safely (§21).

### FR-10 — Citation validation

After generation, the service verifies that every cited `chunkId` was actually among the retrieved chunks. Hallucinated citations are removed and counted as a metric. If no valid citations remain, set `insufficientEvidence = true`.

### FR-11 — Incidents

Users can create troubleshooting incidents with: `id`, `machine_id`, `alarm_code`, `title`, `symptoms`, `status`, `created_at`, `updated_at`.

Statuses: `OPEN`, `IN_PROGRESS`, `RESOLVED`, `CLOSED`, with enforced valid transitions (e.g. `CLOSED` cannot return to `OPEN`).

### FR-12 — Incident history

Store per interaction: question, retrieved chunks with ranks and scores, generated response, model name, prompt version, latencies, final resolution, optional usefulness rating.

### FR-13 — Resolution recording

```json
{ "resolution": "Encoder connector was loose after maintenance.", "resolved": true }
```

The original generated answer must never be overwritten.

### FR-14 — Read-only diagnostic tools

The LLM may call approved mock tools:

```text
get_machine_status(machine_id)
get_active_alarms(machine_id)
get_axis_telemetry(machine_id, axis)
get_maintenance_history(machine_id)
```

Tools use synthetic data, are registered in an explicit allow-list, and have per-call timeouts. No tool may command or alter machinery.

### FR-15 — Tool-call audit trail

Every invocation logs tool name, timestamp, parameters (redacted where needed), result status, and duration — both to logs and to the `tool_execution` table.

### FR-16 — Health endpoints

| Endpoint | Purpose | Checks |
|---|---|---|
| `GET /health/live` | Liveness — is the process up? | None (always 200 if running) |
| `GET /health/ready` | Readiness — can it serve traffic? | DB connection, pgvector extension, embedding model loaded, LLM reachable (or `fake` mode) |

These are used by Docker `HEALTHCHECK`, `docker compose up --wait`, CI smoke tests, and deployment verification.

### FR-17 — API documentation

FastAPI's OpenAPI schema is served at `/openapi.json` and Swagger UI at `/docs`. The CI pipeline exports the schema and fails if it changes without the committed copy being updated (API contract check, §23.2).

### FR-18 — Version endpoint

`GET /version` returns the app version, git commit SHA, build time, prompt version, and model name. The CD pipeline uses it to verify that the deployed build is the expected one.

---

## 12. Initial REST API

Base path: `/api/v1`

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/troubleshoot` | Ask a troubleshooting question |
| `POST` | `/incidents` | Create incident |
| `GET` | `/incidents/{incident_id}` | Retrieve incident |
| `GET` | `/incidents` | List incidents (`status`, `machine_id`, `alarm_code`, `page`, `size`) |
| `PATCH` | `/incidents/{incident_id}/resolution` | Record resolution |
| `POST` | `/documents` | Upload/ingest a document |
| `POST` | `/search` | Retrieval only (no LLM) |

Plus operational endpoints: `/health/live`, `/health/ready`, `/version`, `/docs`, and optionally `/metrics`.

Example troubleshoot request:

```json
{
  "machineId": "CP-01",
  "alarmCode": "SERVO-7021",
  "question": "The servo following error appears during acceleration. What should I check?"
}
```

---

## 13. Domain Model

Use fictional data throughout.

| Entity | Fields |
|---|---|
| **Machine** | id, name, equipment_type, location, manufacturer, model |
| **Incident** | id, machine_id, alarm_code, title, symptoms, status, resolution, created_at, updated_at, resolved_at |
| **Document** | id, name, version, equipment_type, source_type, content_hash, created_at |
| **DocumentChunk** | id (deterministic), document_id, chunk_index, section, content, embedding `vector(384)`, metadata `jsonb` |
| **AIInteraction** | id, incident_id, question, model_name, prompt_version, response `jsonb`, structured_output_valid, repair_attempted, retrieval_ms, generation_ms, total_ms, created_at |
| **RetrievalResult** | id, interaction_id, chunk_id, rank, similarity_score |
| **ToolExecution** | id, interaction_id, tool_name, request `jsonb`, result `jsonb`, duration_ms, status, created_at |

Keep three separate model layers and map between them explicitly:

- **API schemas** (Pydantic) — what crosses the HTTP boundary
- **Domain models** (Pydantic or dataclasses) — what services work with
- **ORM models** (SQLAlchemy) — what is persisted

---

## 14. Non-Functional Requirements

### NFR-01 — Zero required paid services

Core functionality, CI, and CD work without paid services.

### NFR-02 — Reproducibility

A new developer can clone and run:

```bash
make install
make up && make migrate && make ingest
make run
```

Dependencies are locked (`uv.lock`) and CI installs with `uv sync --frozen`, so builds are byte-for-byte reproducible.

### NFR-03 — Configuration

All environment-specific values come from environment variables via pydantic-settings. The repo provides `.env.example`; `.env` is git-ignored.

```env
APP_ENV=local                 # local | ci | staging | production
LOG_LEVEL=INFO
LOG_FORMAT=json               # json | console

DATABASE_URL=postgresql+psycopg://plantassist:local-dev-password@localhost:5432/plantassist

LLM_PROVIDER=ollama           # ollama | fake
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=<model-name>
LLM_TIMEOUT_SECONDS=120

EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
EMBEDDING_DIM=384

RAG_TOP_K=5
RAG_MIN_SCORE=0.70
RAG_CHUNK_SIZE=800
RAG_CHUNK_OVERLAP=120
PROMPT_VERSION=troubleshooting_v1
```

### NFR-04 — Validation

All API input is validated by Pydantic (non-empty question, length limits, valid status, required machine ID, supported document type). Invalid input returns a meaningful 4xx.

### NFR-05 — Error handling

Centralized exception handlers return one consistent shape:

```json
{
  "timestamp": "2026-10-06T16:00:00Z",
  "status": 400,
  "code": "INVALID_REQUEST",
  "message": "question must not be blank",
  "requestId": "3f1c9a..."
}
```

Override FastAPI's default 422 validation response so it uses this shape too.

### NFR-06 — Logging

JSON logs via structlog, with the request ID bound to every log line. Log: request ID, incident ID, retrieval latency, chunks retrieved, LLM latency, model name, prompt version, tool calls, errors. Never log secrets or full document contents.

### NFR-07 — Performance measurement

Record separate timings for retrieval, generation, tool execution, and total request. Store them per interaction and expose them in logs (and optionally Prometheus metrics).

### NFR-08 — Testability and architecture

Business logic lives in services that can be unit tested without FastAPI, a database, or Ollama. External systems sit behind adapter interfaces (`typing.Protocol`). Layering is **enforced in CI** by import-linter, not just documented.

### NFR-09 — Pipeline speed (new)

- PR CI pipeline: target **under 10 minutes** wall-clock.
- Use caching (uv cache, Docker layer cache, embedding model cache) and parallel jobs.
- Slow suites (real-LLM tests) never block PRs; they run nightly or on demand.

---

## 15. Package Structure

```text
src/plantassist/
├── __init__.py               # __version__
├── main.py                   # create_app() factory
├── config.py                 # Settings (pydantic-settings)
├── cli.py                    # Typer: ingest, eval, export-openapi
│
├── api/
│   ├── deps.py               # dependency providers
│   ├── errors.py             # exception handlers, error schema
│   ├── middleware.py         # request ID, timing
│   ├── schemas/              # request/response Pydantic models
│   └── routers/
│       ├── troubleshooting.py
│       ├── incidents.py
│       ├── documents.py
│       ├── search.py
│       └── health.py
│
├── services/
│   ├── troubleshooting_service.py
│   ├── retrieval_service.py
│   ├── ingestion_service.py
│   └── incident_service.py
│
├── domain/
│   ├── models.py
│   ├── enums.py
│   └── errors.py
│
├── rag/
│   ├── parser.py             # Markdown/TXT → sections
│   ├── chunker.py
│   ├── embedder.py           # Embedder protocol + FastEmbedEmbedder
│   ├── context_builder.py
│   └── citation_validator.py
│
├── ai/
│   ├── llm.py                # LLMClient protocol, OllamaClient, FakeLLM
│   ├── structured_output.py  # parse → validate → repair
│   ├── prompts/
│   │   ├── registry.py
│   │   ├── troubleshooting_v1.md
│   │   └── troubleshooting_v2.md
│   └── tools/
│       ├── registry.py       # allow-list, timeouts, audit
│       ├── machine_status.py
│       ├── alarms.py
│       └── maintenance_history.py
│
├── db/
│   ├── session.py
│   ├── orm.py                # SQLAlchemy models
│   └── repositories/
│
├── evaluation/
│   ├── datasets.py
│   ├── retrieval_metrics.py  # Recall@K, Precision@K, MRR
│   ├── answer_metrics.py
│   ├── runner.py
│   └── report.py             # Markdown + JSON reports
│
└── observability/
    ├── logging.py
    └── metrics.py
```

Allowed dependency direction (enforced by import-linter):

```text
api → services → (domain, rag, ai) → db
```

`domain` imports nothing from the other layers. `api` never imports `db` directly.

---

## 16. Repository Structure

```text
industrial-ai-troubleshooting/
├── README.md
├── PROJECT_REQUIREMENTS.md
├── CHANGELOG.md                     # generated by release-please
├── LICENSE
├── pyproject.toml                   # deps + ruff + mypy + pytest + coverage config
├── uv.lock
├── Makefile
├── Dockerfile
├── .dockerignore
├── docker-compose.yml               # postgres (+ app, + optional ollama)
├── docker-compose.ci.yml            # CI overrides (built image, LLM_PROVIDER=fake)
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── .importlinter
├── alembic.ini
├── migrations/
│   └── versions/
│
├── src/plantassist/                 # see §15
│
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── ai/
│
├── sample-data/
│   ├── manuals/
│   ├── incidents/
│   └── machines/
│
├── evaluation/
│   ├── questions.json
│   ├── ground_truth.json
│   └── baseline.json                # committed quality baseline (§24.3)
│
├── openapi/
│   └── openapi.json                 # committed API contract
│
├── docs/
│   ├── architecture.md
│   ├── pipelines.md                 # how every pipeline works
│   ├── evaluation.md
│   ├── runbook.md                   # deploy, rollback, troubleshooting
│   ├── api-examples.md
│   └── adr/                         # Architecture Decision Records
│       ├── 001-explicit-rag-over-framework.md
│       ├── 002-github-actions-ci.md
│       └── ...
│
└── .github/
    ├── workflows/
    │   ├── ci.yml
    │   ├── release.yml
    │   ├── deploy.yml
    │   ├── eval-llm.yml
    │   ├── codeql.yml
    │   └── docs.yml
    ├── actions/
    │   └── setup-python-env/action.yml   # composite action
    ├── dependabot.yml
    ├── CODEOWNERS
    └── pull_request_template.md
```

---

## 17. Data Strategy

Do not use confidential workplace material. Use synthetic manuals written for this project, fictional alarm tables and maintenance records, and openly licensed material only where the license allows redistribution.

### Starter corpus

Equipment categories:

1. Servo drive
2. Conveyor
3. Photoelectric sensor
4. Pneumatic cylinder
5. Safety circuit

For each category: an operating guide, an alarm/fault table, a troubleshooting section, a maintenance procedure, and 5–10 synthetic incident records.

### Data validation in CI

The corpus is treated like code. CI validates that:

- every document has valid front matter (Pydantic schema)
- every document declares `license: synthetic` or an approved open license
- every chunk ID referenced in `evaluation/ground_truth.json` exists after ingestion
- no duplicate `document_id` values exist

---

## 18. RAG Pipeline

### Ingestion time

```text
Source files
   ↓  discover
Front-matter validation ──✗──► reject + report
   ↓
Content hash ──unchanged──► skip
   ↓
Parser (sections)
   ↓
Chunker (size/overlap from config)
   ↓
Metadata enrichment + deterministic chunk IDs
   ↓
fastembed (batched)
   ↓
Transactional upsert → PostgreSQL/pgvector
   ↓
Ingestion report (counts, duration)
```

### Query time

```text
Question → query embedding → pgvector similarity search → top-K chunks
   → min-score filter ──none left──► insufficientEvidence = true
   → context builder → versioned prompt + evidence → LLM (JSON schema)
   → Pydantic validation ──invalid──► repair retry ──still invalid──► safe fallback
   → citation validation → persist interaction → API response
```

---

## 19. Retrieval Evaluation

Retrieval is evaluated separately from generation, because it is fast, deterministic, and runs on CPU — **which means it can run in CI on every PR.**

Ground truth example:

```json
{
  "id": "ret-001",
  "question": "What can cause a servo following error during acceleration?",
  "relevantChunkIds": [
    "servo-manual-v1:following-error:001",
    "servo-manual-v1:following-error:002"
  ]
}
```

Metrics:

| Metric | Question it answers |
|---|---|
| Recall@K (K = 1, 3, 5) | Did a correct chunk appear in the top K? |
| Precision@K | What share of retrieved chunks were relevant? |
| MRR | How high did the first correct chunk rank? |
| Retrieval latency (p50/p95) | How fast is search? |

---

## 20. LLM Evaluation

Do not stop at "it looks like it works." Build an evaluation set of **30–50 questions** for the MVP:

```json
{
  "id": "eval-001",
  "question": "What should be checked after a servo following error begins immediately after maintenance?",
  "expectedSources": ["servo-manual-v1:following-error:002"],
  "expectedConcepts": ["mechanical alignment", "encoder connection", "axis binding"],
  "expectInsufficientEvidence": false
}
```

Include negative cases (questions the corpus cannot answer) to measure refusal behavior.

Metrics:

| Metric | How it is measured |
|---|---|
| Structured-output validity rate | % of responses that pass Pydantic validation (before and after repair) |
| Citation accuracy | % of cited chunks that were retrieved and are in `expectedSources` |
| Hallucinated-citation rate | % of citations removed by the citation validator |
| Concept coverage | % of `expectedConcepts` present (keyword/embedding similarity) |
| Insufficient-evidence accuracy | Correct refusals on negative cases |
| Groundedness (optional) | LLM-as-judge using the local model, clearly labeled as approximate |
| Generation latency (p50/p95) | Timing |

Results are written as JSON + Markdown reports and published (§24).

---

## 21. Structured Output Reliability

Goal: make LLM behavior reliable enough for software to consume.

On every call:

1. Request output constrained to the Pydantic JSON schema (Ollama `format=`).
2. Validate with `TroubleshootingResponse.model_validate_json(...)`.
3. On failure: capture the error, retry once with a repair prompt that includes the validation errors.
4. Record `structured_output_valid` and `repair_attempted` on the interaction.
5. If still invalid: return a safe fallback response (`insufficientEvidence: true`, sources from retrieval, clear message). **Never return a 500 because of malformed model output.**

Track: `valid structured output rate = valid / total` (e.g. `47 / 50 = 94%`), before and after repair.

---

## 22. Engineering Principles

### 22.1 CI parity

Anything CI runs, a developer can run locally with the same `make` target. Workflows contain orchestration, not logic.

### 22.2 Layered architecture, enforced

```text
Routers (thin) → Services (business logic) → Domain / RAG / AI → Repositories / adapters
```

Routers do not contain business logic. import-linter fails the build if layers are crossed.

### 22.3 Ports and adapters for external systems

`LLMClient`, `Embedder`, and repositories are `Protocol`s. Production uses Ollama/fastembed/PostgreSQL; tests use fakes. This is what makes the CI pipeline fast and deterministic.

### 22.4 Configuration over hard-coding

Models, thresholds, URLs, top-K, chunk sizes, and prompt versions are configuration.

### 22.5 Test behavior, not implementation details

### 22.6 Prefer explicit code

This project demonstrates engineering skill; don't hide the pipeline behind framework magic.

### 22.7 Everything as code

Infrastructure (Compose), pipelines (workflows), quality thresholds (`baseline.json`, coverage config), dependency updates (`dependabot.yml`), and decisions (ADRs) all live in the repository and change through pull requests.

---

## 23. CI Pipeline (every pull request and push to `main`)

This is the core learning section. Build it incrementally (§30), but this is the target.

### 23.1 Pipeline stages

```text
                       ┌──────────────┐
            ┌────────► │ lint         │ ruff, format check, import-linter
            │          ├──────────────┤
            ├────────► │ typecheck    │ mypy --strict src
            │          ├──────────────┤
 PR opened ─┼────────► │ unit tests   │ matrix: py3.12, py3.13 · coverage gate
            │          ├──────────────┤
            ├────────► │ security     │ pip-audit, bandit, gitleaks
            │          └──────┬───────┘
            │                 ▼
            │          ┌──────────────┐
            ├────────► │ integration  │ Testcontainers pgvector · alembic up/down/check
            │          ├──────────────┤
            ├────────► │ contracts    │ OpenAPI diff · corpus/eval-set validation
            │          ├──────────────┤
            ├────────► │ retrieval    │ ingest sample corpus · Recall@K/MRR · regression gate
            │          │ eval         │
            │          ├──────────────┤
            └────────► │ image        │ buildx (cached) · Trivy scan · compose smoke + e2e (FakeLLM)
                       └──────┬───────┘
                              ▼
                       ┌──────────────┐
                       │ ci-success   │ single required status check
                       └──────────────┘
```

### 23.2 Jobs and quality gates

| Job | Tools | Gate (fails the PR if…) |
|---|---|---|
| `lint` | ruff check, ruff format --check, import-linter | any violation |
| `typecheck` | mypy | any error |
| `unit` | pytest -m unit, pytest-cov | any failure; coverage < 80% on `services/`, `rag/`, `ai/`, `domain/` |
| `security` | pip-audit, bandit, gitleaks | known vulnerable dependency (high+); bandit high; any detected secret |
| `integration` | pytest -m integration, testcontainers | any failure |
| `migrations` | `alembic upgrade head`, `alembic downgrade -1`, `alembic upgrade head`, `alembic check` | migration fails, or ORM models drift from migrations |
| `contracts` | export OpenAPI and `git diff --exit-code`; corpus validator | API changed without updating `openapi/openapi.json`; invalid corpus or eval set |
| `retrieval-eval` | `plantassist eval retrieval` | Recall@5 or MRR drops below `baseline.json` minus tolerance |
| `image` | docker buildx, Trivy | build fails; CRITICAL image vulnerabilities with a fix available |
| `smoke-e2e` | docker compose (`--wait`), curl, pytest -m e2e | readiness fails; end-to-end flow fails with FakeLLM |
| `ci-success` | aggregator job | any needed job failed or was cancelled |

### 23.3 Professional practices to implement in the workflows

- **Least-privilege tokens:** set `permissions: contents: read` at the top of every workflow; grant more per job only when needed.
- **Pin third-party actions to a commit SHA** (with a version comment); Dependabot keeps them updated.
- **Concurrency control:** cancel superseded runs on the same branch.
- **Caching:** uv cache (via `setup-uv`), Docker layers (`type=gha`), fastembed model directory.
- **Composite action** `.github/actions/setup-python-env` so setup logic is written once.
- **Reusable workflow** (`workflow_call`) for build-and-scan, shared by `ci.yml` and `release.yml`.
- **Path filters:** docs-only changes skip heavy jobs (but `ci-success` still reports).
- **Artifacts:** upload coverage XML, JUnit XML, evaluation reports, and Trivy SARIF.
- **Job summaries:** write metrics tables to `$GITHUB_STEP_SUMMARY` so results show on the run page.
- **Code scanning:** upload Trivy and CodeQL SARIF to GitHub's Security tab.
- **Timeouts:** every job has `timeout-minutes`.

### 23.4 Shift-left: local hooks

`.pre-commit-config.yaml` runs on every commit: ruff (lint + format), mypy on changed files, gitleaks, end-of-file/whitespace fixers, and a check that `uv.lock` is in sync. CI also runs `pre-commit run --all-files` so skipped hooks are still caught.

### 23.5 Repository governance

Configure a **branch ruleset** on `main`:

- Pull request required (no direct pushes)
- Required status check: `ci-success`
- Branch must be up to date before merging
- Linear history (squash merges)
- Conventional Commit PR titles, enforced by a PR-title check

Also add `CODEOWNERS`, a pull request template (what/why/how tested/eval impact), and issue templates. Even solo, work through issues → branches → PRs so the repo history looks like a team's.

---

## 24. Evaluation Pipeline (ML-quality CI)

### 24.1 Split by cost

| Evaluation | Needs LLM? | Runs | Blocks merge? |
|---|---|---|---|
| Retrieval eval (Recall@K, MRR) | No | Every PR | **Yes** — regression gate |
| E2E flow with FakeLLM | No | Every PR | **Yes** |
| LLM answer eval — smoke subset (5–10 questions, tiny model) | Yes | Nightly + manual + PR label `run-llm-eval` | No (reports only) |
| LLM answer eval — full set (30–50 questions, real model) | Yes | Manually on your machine, before releases | Release checklist |

### 24.2 `eval-llm.yml` workflow

- Triggers: `schedule` (nightly), `workflow_dispatch` (with inputs: model, prompt version, subset size), and PRs labeled `run-llm-eval`.
- Steps: start Postgres → install Ollama on the runner → restore the model from `actions/cache` (or pull) → ingest corpus → run eval → upload JSON/Markdown report → post a summary comment on the PR (if PR-triggered) → append results to history.
- CPU-only runners are slow; keep the CI subset small and the model tiny. The goal here is to prove the **pipeline**, not to benchmark the model.

### 24.3 Baselines and regression gates

`evaluation/baseline.json` holds the accepted metrics:

```json
{
  "retrieval": { "recall_at_5": 0.88, "mrr": 0.71, "tolerance": 0.02 },
  "llm": { "schema_valid_rate": 0.94, "citation_accuracy": 0.85 },
  "embedding_model": "BAAI/bge-small-en-v1.5",
  "updated_at": "2026-10-06"
}
```

(Values above are placeholders — replace with your measured numbers.)

Rules:

- CI fails if a PR makes retrieval metrics worse than baseline − tolerance.
- Improving the baseline requires a PR that changes `baseline.json`, so every quality change is reviewed and recorded in history.
- Prompt changes (`troubleshooting_v1` → `v2`) must include an eval report comparing both versions in the PR description.

### 24.4 Publishing results

`docs.yml` builds a small static site (MkDocs or plain HTML) with architecture docs and an **evaluation history chart**, and deploys it to GitHub Pages. Recruiters can see quality metrics over time without cloning anything.

### 24.5 Pipeline triggers tied to data

Changes under `sample-data/**`, `evaluation/**`, `src/plantassist/rag/**`, or `src/plantassist/ai/prompts/**` always trigger the retrieval eval and add the `needs-llm-eval` label automatically.

---

## 25. CD / Release Pipeline

### 25.1 Versioning and releases

- **Conventional Commits** (`feat:`, `fix:`, `docs:`, `test:`, `ci:`, `refactor:`, `chore:`).
- **release-please** runs on every push to `main` and maintains a release PR that bumps the version (Semantic Versioning) and updates `CHANGELOG.md`.
- Merging the release PR creates a git tag (`v1.4.0`) and a GitHub Release.
- The version is single-sourced (`pyproject.toml`) and surfaced at `GET /version`.

### 25.2 Artifact build (`release.yml`)

On a published release:

1. Call the reusable build-and-scan workflow.
2. Build the image with build args `VERSION`, `GIT_SHA`, `BUILD_DATE`, and OCI labels.
3. Tag: `ghcr.io/<owner>/plantassist:1.4.0`, `:1.4`, `:sha-<short>`, `:latest`.
4. Generate an **SBOM** (Syft, SPDX JSON) and attach it to the release.
5. **Sign** the image with Cosign keyless signing (GitHub OIDC; needs `id-token: write`).
6. Push to GHCR.

On every merge to `main` (not just releases), also publish `:main` and `:sha-<short>` images so staging can deploy continuously.

### 25.3 Environments

| Environment | Where | How it's deployed | Gate |
|---|---|---|---|
| `local` | Developer laptop | `docker compose up` | — |
| `ci` | Ephemeral, inside the CI runner | Compose with locally built image + FakeLLM | Automatic |
| `staging` | Ephemeral, fresh GitHub runner | Pull the **published** image from GHCR, run migrations, ingest corpus, run smoke + E2E | Automatic after image publish |
| `production` | Your own machine (self-hosted runner) **or** "verified release" only | See §25.4 | **Manual approval** via GitHub Environment protection rules |

Staging tests the exact artifact that was published — not a rebuild. This is the "build once, deploy many" principle.

### 25.4 Production deployment options ($0)

**Option A — Self-hosted runner on your own machine (recommended for learning)**

- Register a self-hosted runner on your laptop/desktop/home server with the label `plantassist-prod`.
- `deploy.yml` job targets `runs-on: [self-hosted, plantassist-prod]` and the `production` environment (required reviewer: you).
- Steps: verify the image signature with Cosign → `docker compose pull` the pinned version → run Alembic migrations → `docker compose up -d --wait` → verify `/health/ready` and `/version` return the expected SHA → run post-deploy smoke tests.
- On failure: automatically redeploy the previous version (stored in a `.deployed-version` file) and fail the job.

**Security rules for Option A (mandatory on a public repo):**

- Never run the self-hosted runner on `pull_request` events — fork PRs could execute code on your machine.
- Only the `deploy.yml` workflow uses it, triggered by `release` / `workflow_dispatch` on `main`, behind the `production` environment approval.
- Run the runner as a non-admin user, ideally inside a VM or dedicated user account.
- In repo settings, require approval for workflows from outside contributors.

**Option B — Verified release (no machine needed)**

If you don't want a runner on your machine, "production" means: the signed, scanned, staging-verified image is published and promoted with a `:stable` tag after manual approval. Document how a user deploys it with Compose.

### 25.5 Database migrations in CD

- Migrations run as a separate step before the new app version starts.
- Migrations must be backward-compatible with the previous app version (expand → migrate → contract), so rollback of the app doesn't require rolling back the schema.
- Back up the production database (`pg_dump`) before migrating; keep the last N dumps.

### 25.6 Rollback

- `deploy.yml` accepts a `version` input; redeploying an older tag is the rollback.
- `docs/runbook.md` documents manual rollback steps, how to restore a DB dump, and how to read deployment logs.

### 25.7 Delivery metrics (resume material)

Track simple DORA-style metrics from GitHub data: deployment frequency, lead time from merge to deploy, change failure rate (failed deploys / total), and time to restore (rollback duration). A short script using the `gh` CLI can compute them into the docs site.

---

## 26. Supply Chain and Dependency Management

- **Dependabot** (`.github/dependabot.yml`) for `uv`/pip dependencies, GitHub Actions, and Docker base images, grouped weekly to limit noise.
- Dependabot PRs go through the full CI pipeline, including the retrieval-eval gate — a dependency upgrade that hurts retrieval quality gets caught.
- `pip-audit` against the lockfile on every PR and on a weekly schedule.
- **CodeQL** analysis for Python (free on public repos).
- Base image pinned by digest in the Dockerfile; Dependabot updates the digest.
- SBOM attached to every release; images signed with Cosign.
- Optional: enable OpenSSF Scorecard and display the badge.

---

## 27. Docker Requirements

### Dockerfile (multi-stage)

- **Builder stage:** official Python slim image + uv; `uv sync --frozen --no-dev` into `/app/.venv`; download the fastembed model into the image so containers start without network access.
- **Runtime stage:** slim image, copy only the venv, source, migrations, and model cache; run as a **non-root user**; `HEALTHCHECK` hitting `/health/live`; OCI labels (`org.opencontainers.image.source`, `version`, `revision`).
- `.dockerignore` excludes `.git`, `.venv`, tests, caches, `.env`.

### Compose

`docker-compose.yml` services:

- `postgres` — `pgvector/pgvector` image, named volume, healthcheck (`pg_isready`)
- `app` — the built image, `depends_on: postgres: condition: service_healthy`
- `migrate` — one-shot service running `alembic upgrade head`
- `ollama` — optional profile (`--profile ollama`) for those who want it containerized

`docker-compose.ci.yml` overrides the app image tag and sets `LLM_PROVIDER=fake`.

Target commands:

```bash
docker compose up -d --wait                    # postgres only, dev mode
docker compose --profile app up --build --wait # full stack
```

Ollama on the host is the default (avoids GPU passthrough complexity); from inside a container, reach it at `http://host.docker.internal:11434` (add `extra_hosts: ["host.docker.internal:host-gateway"]` on Linux). Document both approaches.

---

## 28. Testing Strategy

### Test pyramid and markers

| Marker | Scope | Speed | Needs | Runs in |
|---|---|---|---|---|
| `unit` | Services, chunker, parser, metrics, prompt building, structured-output repair, state transitions | ms | nothing | pre-commit (changed), every PR |
| `integration` | Repositories, migrations, vector search, ingestion end-to-end | seconds | Docker | every PR |
| `e2e` | Full HTTP flow against the running container stack | seconds | Docker, FakeLLM | every PR |
| `ai` | Real Ollama: prompt behavior, tool calling | minutes | Ollama | nightly / manual |

Register markers in `pyproject.toml` with `--strict-markers` so typos fail.

### Specific techniques

- **Property-based tests** (Hypothesis) for the chunker: no text lost, overlap respected, chunk IDs deterministic, no chunk exceeds max size.
- **respx** to simulate Ollama responses: valid JSON, invalid JSON, timeout, connection refused, tool-call responses.
- **FakeLLM** returns deterministic, schema-valid responses that cite the retrieved chunks — lets E2E tests exercise the full RAG path in CI.
- **Testcontainers** session-scoped PostgreSQL+pgvector fixture with per-test transaction rollback for isolation.
- **API tests** with `httpx.AsyncClient(transport=ASGITransport(app=app))` and `app.dependency_overrides` for fakes.

---

## 29. Failure Cases to Handle (and test)

| Failure | Expected behavior | Test level |
|---|---|---|
| Ollama unavailable | 503 with `LLM_UNAVAILABLE`; readiness reports LLM down; no crash | unit (respx) + integration |
| Ollama timeout | 504 / controlled error; latency logged | unit |
| PostgreSQL unavailable | Readiness fails; controlled 503 | integration |
| No relevant documents | `insufficientEvidence: true`, no fabricated answer | unit + e2e |
| Invalid LLM schema | Repair retry → safe fallback; metrics recorded | unit |
| Hallucinated citation | Removed by citation validator; counted | unit |
| Tool timeout / error | Continue without tool data and say so | unit |
| Empty document | Ingestion rejects with clear error | unit |
| Unsupported file type | 415/422 with clear message | API test |
| Oversized upload | 413 | API test |
| Embedding dimension mismatch | Fail fast at startup | integration |

---

## 30. Security Requirements

- Validate uploads: allowed extensions + content sniffing, size limit, sanitized filenames, never execute or eval content, prevent path traversal (resolve and check against the upload root).
- All DB access through SQLAlchemy with bound parameters; no string-built SQL.
- Secrets only from environment variables; `.env` git-ignored; gitleaks in pre-commit and CI.
- Never log passwords, tokens, or full document contents.
- CI secrets: none needed for the core pipeline (GHCR uses the built-in `GITHUB_TOKEN`; Cosign uses OIDC). If any are ever added, scope them to environments.
- Stretch: API key or OAuth2 password flow with roles `TECHNICIAN`, `ENGINEER`, `ADMIN` (FastAPI security utilities). Not required for MVP.

---

## 31. Observability Requirements

Minimum:

- JSON structured logs (structlog) with request ID on every line
- Request ID returned in the `X-Request-ID` response header
- Liveness/readiness endpoints
- Per-request timings: retrieval, generation, tools, total

Optional (only if it adds value):

- `/metrics` via `prometheus-fastapi-instrumentator`, plus custom counters (structured-output failures, hallucinated citations, insufficient-evidence responses)
- Prometheus + Grafana via a Compose profile, with a dashboard JSON committed to the repo
- OpenTelemetry tracing (retrieval and LLM spans)

---

## 32. MVP Definition

The project reaches MVP when all of the following work:

**Application**

- [ ] FastAPI app starts and serves `/docs`
- [ ] PostgreSQL + pgvector runs in Docker; Alembic migrations apply cleanly
- [ ] Synthetic documents are ingested idempotently with deterministic chunk IDs
- [ ] Embeddings are generated locally and stored in pgvector
- [ ] `/search` returns top-K chunks with scores and sources
- [ ] Ollama generates an answer mapped to a Pydantic model, with repair/fallback
- [ ] Citations are validated and returned
- [ ] Incidents and AI interactions are persisted
- [ ] Centralized error handling returns the standard error shape

**Pipelines**

- [ ] pre-commit hooks installed and passing
- [ ] CI runs lint, types, unit, integration, security, and image build on every PR
- [ ] Retrieval evaluation runs in CI with a baseline regression gate
- [ ] Branch protection requires `ci-success`
- [ ] Merges to `main` publish a versioned image to GHCR
- [ ] README explains how to reproduce everything
- [ ] No paid service is required

---

## 33. Development Phases

Every phase delivers **application work and pipeline work together.** The pipeline is never "added at the end."

### Phase 0 — Walking skeleton (pipeline first)

*Goal: a trivial app that already travels through a real pipeline.*

App:
- uv project, `src/` layout, `create_app()` factory
- `/health/live` and `/version` endpoints
- pydantic-settings config, structlog logging
- One unit test

Pipeline:
- `Makefile` with `install`, `lint`, `typecheck`, `test-unit`, `run`
- pre-commit with ruff + gitleaks
- `ci.yml`: lint → typecheck → unit tests (one Python version)
- Branch ruleset on `main` requiring CI; Conventional Commit PR titles

**Deliverable:** green CI badge on a PR-based repository. *Learning focus: GitHub Actions basics — triggers, jobs, steps, runners, caching.*

### Phase 1 — Incident API + database

App:
- PostgreSQL in Compose; SQLAlchemy models; Alembic migrations
- Incident CRUD + resolution + status transitions
- Error handler, validation, pagination

Pipeline:
- Integration tests with Testcontainers
- `migrations` job (upgrade/downgrade/check)
- Coverage report + coverage gate
- Python version matrix (3.12, 3.13)
- Composite setup action to remove duplication

**Deliverable:** a solid Python backend with a real test pyramid. *Learning focus: service containers vs Testcontainers, matrices, artifacts, composite actions.*

### Phase 2 — Containerization + CD foundation

App:
- Multi-stage Dockerfile, non-root, healthcheck
- Readiness endpoint with DB check

Pipeline:
- `image` job: buildx with GHA cache, Trivy scan, SARIF upload
- Compose smoke test in CI (`up --wait` + curl)
- Publish `:main` and `:sha-*` images to GHCR on merge
- release-please + CHANGELOG + semver tags
- Dependabot + CodeQL

**Deliverable:** every merge produces a scanned, versioned, published container. *Learning focus: container builds in CI, registries, permissions, release automation.*

### Phase 3 — Document ingestion pipeline

App:
- Front-matter schema, parser, chunker (with Hypothesis tests)
- Deterministic chunk IDs, content hashing, transactional upsert
- `plantassist ingest` CLI + ingestion report

Pipeline:
- Corpus validation job (`contracts`)
- Path filters so corpus changes trigger the right jobs

**Deliverable:** idempotent, validated data pipeline. *Learning focus: data pipelines as code, path-based triggers.*

### Phase 4 — Embeddings, pgvector, retrieval evaluation

App:
- fastembed embedder, pgvector column + index
- `/search` endpoint, min-score filtering
- Ground-truth set + Recall@K/Precision@K/MRR

Pipeline:
- `retrieval-eval` job with model caching
- `baseline.json` regression gate
- Metrics table in the job summary

**Deliverable:** measurable retrieval quality that can't silently regress. *Learning focus: ML quality gates in CI.*

### Phase 5 — Local LLM + full RAG

App:
- `LLMClient` protocol, `OllamaClient`, `FakeLLM`
- Versioned prompts, structured output with repair/fallback
- Citation validator, insufficient-evidence behavior
- Persist AI interactions with timings

Pipeline:
- E2E tests in CI against the container stack using FakeLLM
- `ai`-marked tests excluded from PR CI
- OpenAPI contract check

**Deliverable:** source-grounded troubleshooting assistant, fully tested in CI without an LLM. *Learning focus: test doubles as a pipeline-speed strategy, contract testing.*

### Phase 6 — LLM evaluation pipeline

App:
- 30–50 question eval set incl. negative cases
- Answer metrics, prompt v1 vs v2 comparison

Pipeline:
- `eval-llm.yml` (nightly + manual + PR label) with Ollama on the runner
- PR comment with eval summary
- `docs.yml` publishes eval history to GitHub Pages

**Deliverable:** quantitative AI results published automatically. *Learning focus: scheduled workflows, workflow_dispatch inputs, PR automation, Pages.*

### Phase 7 — Tool calling

App:
- Mock tools, allow-list registry, timeouts, audit trail
- Tool-calling loop with Ollama

Pipeline:
- Unit tests with respx-simulated tool-call responses
- Tool-calling cases added to the nightly LLM eval

**Deliverable:** AI combines documents with simulated machine data. 

### Phase 8 — Production deployment

Pipeline:
- `deploy.yml`: staging (ephemeral, published image) → manual approval → production
- Self-hosted runner (Option A) or verified release (Option B)
- Cosign signing + verification, SBOM on releases
- Automated rollback, `runbook.md`
- Delivery metrics script

**Deliverable:** a complete build → test → release → deploy → verify → rollback loop. *Learning focus: environments, approvals, OIDC, supply-chain security, rollback.*

### Phase 9 — Optional UI and observability

- Simple dashboard: troubleshooting form, sources, incident history, resolution form
- Optional Prometheus/Grafana profile

---

## 34. Stretch Goals

Only after the core system and pipelines are solid:

- Hybrid retrieval (pgvector + PostgreSQL full-text search with rank fusion)
- Reranking with a small local cross-encoder
- Conversation memory per incident
- Helpful / Not helpful feedback feeding the eval set
- Multi-query retrieval
- LangChain or LlamaIndex adapter behind the existing `LLMClient`/retriever interfaces
- Authentication and roles
- Streaming responses via Server-Sent Events
- Preview environments: deploy each PR's image to an ephemeral stack and post its smoke-test results
- Load testing (Locust) in a manual workflow with p95 latency reported

---

## 35. Features NOT to Add Early

- Kubernetes / Helm
- Kafka or message queues
- Microservices
- Multiple LLM providers
- Paid cloud deployment
- Terraform for cloud resources you don't need
- Complex React frontend
- Real PLC connections or autonomous equipment control
- Multi-agent orchestration
- Large-scale distributed vector infrastructure

A clean monolith with a professional pipeline beats an over-engineered, unfinished system.

---

## 36. Git Strategy

**Trunk-based development** with short-lived branches and squash merges:

```text
main
feat/incident-api
feat/ingestion-pipeline
feat/vector-search
ci/retrieval-eval-gate
feat/rag
feat/tool-calling
ci/deploy-workflow
```

Commit/PR title examples:

```text
feat(incidents): add incident persistence layer
feat(rag): implement pgvector semantic retrieval
test(rag): add property-based tests for chunker
ci: add retrieval evaluation regression gate
ci(release): sign images with cosign
fix(ai): handle malformed structured LLM responses
docs: add local Ollama setup instructions
```

Workflow: open an issue → branch → PR using the template → CI green → squash merge → release-please updates the release PR.

---

## 37. Definition of Done (per feature)

A feature is done when:

- [ ] Implementation works and has validation and error handling
- [ ] Unit/integration/e2e tests added where appropriate
- [ ] CI is green, including coverage and eval gates
- [ ] Type checks pass
- [ ] Configuration is documented in `.env.example`
- [ ] OpenAPI contract updated if the API changed
- [ ] README/docs/ADR updated if behavior or architecture changed
- [ ] Merged via PR with a Conventional Commit title

---

## 38. README Requirements

1. Project summary and badges (CI, coverage, latest release, Pages)
2. Why it was built
3. Architecture diagram (runtime **and** delivery)
4. Technology stack
5. Features
6. Screenshots / demo GIF
7. Local setup (`make` targets)
8. Docker setup
9. Example API calls
10. RAG explanation
11. Tool-calling explanation
12. **CI/CD pipeline explanation** (stages, gates, environments, how to release, how to roll back)
13. Evaluation methodology
14. Quantitative results (linked to the Pages report)
15. Limitations and safety boundary
16. Future improvements

---

## 39. Resume Success Criteria

Do not write resume metrics until they are measured. **Never fabricate values.**

Examples of the *type* of bullet the project should support:

> Built a Python/FastAPI industrial troubleshooting assistant using local LLM inference (Ollama), PostgreSQL/pgvector, and RAG, returning schema-validated, source-cited responses.

> Designed a GitHub Actions CI/CD pipeline with linting, strict typing, Testcontainers integration tests, container vulnerability scanning, and an automated retrieval-quality gate (Recall@5 ≥ **X**) that blocks regressions on every pull request.

> Automated releases with semantic versioning, SBOM generation, signed container images, staged deployment with manual approval, and automated rollback — **N** releases with a **Y%** change-failure rate.

> Built an LLM evaluation pipeline over **N** queries tracking schema validity (**X%**), citation accuracy (**Y%**), and latency, improving **metric A from X to Y** between prompt versions.

---

## 40. Portfolio Success Criteria

Someone viewing the repository should quickly see evidence of:

- Python backend engineering with clean, enforced architecture
- REST API design and SQL/migration skills
- LLM integration, RAG, vector search, structured outputs
- Data pipeline design (idempotent, validated ingestion)
- ML evaluation with quality gates
- Automated testing across the pyramid
- **A complete CI/CD pipeline: green checks on PRs, published releases, signed images, deployment history**
- Docker, observability, and production-minded error handling
- Clear documentation, runbook, and ADRs

---

## 41. Free-Only Design Decisions

| Decision | Instead of |
|---|---|
| Ollama local LLM | Paid LLM APIs |
| fastembed local ONNX embeddings | Paid embedding APIs |
| PostgreSQL + pgvector in Docker | Hosted vector DB |
| GitHub Actions on a public repo | Paid CI |
| GHCR public images | Paid registry |
| Self-hosted runner / verified release | Paid cloud hosting |
| GitHub Pages for reports | Paid dashboards |
| Synthetic data | Paid or proprietary datasets |

---

## 42. Initial Acceptance Tests

| # | Scenario | Expected |
|---|---|---|
| 1 | Servo following-error question | Relevant servo chunks retrieved; structured response; ≥ 1 valid citation; HTTP 200 |
| 2 | Question unrelated to the corpus | `insufficientEvidence: true`; no detailed fabricated answer |
| 3 | Ollama unavailable | Controlled 503; no crash; readiness reports LLM down |
| 4 | `{"question": ""}` | HTTP 400 with validation message in the standard error shape |
| 5 | Create incident, restart app | Incident still available |
| 6 | Run retrieval eval | Recall@1, Recall@3, Recall@5, MRR reported; CI fails if below baseline |
| 7 | Ingest the same corpus twice | Second run: all documents skipped, zero changes |
| 8 | PR that breaks a migration | `migrations` job fails; PR cannot merge |
| 9 | PR that changes the API without updating `openapi.json` | `contracts` job fails |
| 10 | Merge to `main` | Image published to GHCR with `:sha-*` tag; staging smoke tests pass against it |
| 11 | Deploy a bad version | Post-deploy verification fails; previous version restored automatically |

---

## 43. First Development Target

Before touching any AI code, complete **Phase 0 and Phase 1**:

```text
GET   /health/live
GET   /version
POST  /api/v1/incidents
GET   /api/v1/incidents/{id}
GET   /api/v1/incidents
PATCH /api/v1/incidents/{id}/resolution
```

with PostgreSQL, Alembic, SQLAlchemy, validation, error handling, unit tests, integration tests — **and a CI pipeline that runs all of it on every pull request.**

This forces the project to start as a strong Python backend with a professional delivery pipeline, rather than an LLM wrapper.

---

## 44. Final Constraint Checklist

Before adding any dependency, service, or workflow, ask:

- [ ] Can this be used without paying?
- [ ] Can another developer reproduce it locally (`make` target)?
- [ ] Does CI run it, and does it fail loudly when broken?
- [ ] Does it improve the resume story?
- [ ] Can we test it, and can we measure its value?
- [ ] Does it avoid proprietary data?
- [ ] Is it necessary for the current phase?

If the answer is no, do not add it yet.

---

## Appendix A — Reference `ci.yml` Skeleton

A starting point for Phase 0–4. Action versions are illustrative; pin each to a commit SHA in the real file and let Dependabot update them.

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python-env
      - run: make lint typecheck

  unit:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python-env
        with:
          python-version: ${{ matrix.python-version }}
      - run: make test-unit
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: unit-reports-${{ matrix.python-version }}
          path: reports/

  integration:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python-env
      - run: make test-integration   # Testcontainers starts pgvector
      - run: make migrations-check   # upgrade, downgrade -1, upgrade, alembic check

  security:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0              # gitleaks scans history
      - uses: ./.github/actions/setup-python-env
      - run: make security

  retrieval-eval:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    needs: [unit]
    steps:
      - uses: actions/checkout@v4
      - uses: ./.github/actions/setup-python-env
      - uses: actions/cache@v4
        with:
          path: ~/.cache/plantassist/models
          key: embed-${{ hashFiles('src/plantassist/config.py') }}
      - run: make eval-retrieval      # exits non-zero below baseline - tolerance
      - if: always()
        run: cat reports/retrieval_eval.md >> "$GITHUB_STEP_SUMMARY"

  image:
    runs-on: ubuntu-latest
    timeout-minutes: 25
    needs: [unit, integration]
    permissions:
      contents: read
      security-events: write          # upload Trivy SARIF
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          load: true
          tags: plantassist:ci
          cache-from: type=gha
          cache-to: type=gha,mode=max
      - uses: aquasecurity/trivy-action@master   # pin to a SHA
        with:
          image-ref: plantassist:ci
          severity: CRITICAL
          ignore-unfixed: true
          exit-code: "1"
      - run: make smoke                # compose up --wait with docker-compose.ci.yml, curl health
      - run: make test-e2e             # full RAG flow with LLM_PROVIDER=fake

  ci-success:
    if: always()
    needs: [lint, unit, integration, security, retrieval-eval, image]
    runs-on: ubuntu-latest
    steps:
      - name: Fail if any required job did not succeed
        if: contains(needs.*.result, 'failure') || contains(needs.*.result, 'cancelled')
        run: exit 1
```

Composite action `.github/actions/setup-python-env/action.yml`:

```yaml
name: Set up Python environment
inputs:
  python-version:
    default: "3.12"
runs:
  using: composite
  steps:
    - uses: astral-sh/setup-uv@v6
      with:
        python-version: ${{ inputs.python-version }}
        enable-cache: true
    - run: uv sync --frozen --all-groups
      shell: bash
```

---

## Appendix B — Learning Map: Pipeline Concepts by Phase

| Concept | Where you learn it |
|---|---|
| Triggers, jobs, steps, runners | Phase 0 |
| Caching, artifacts, matrices | Phase 1 |
| Composite actions, reusable workflows | Phase 1–2 |
| Service containers vs Testcontainers | Phase 1 |
| Docker in CI, layer caching, registries | Phase 2 |
| Least-privilege `permissions`, `GITHUB_TOKEN` | Phase 2 |
| Semantic versioning, changelogs, release automation | Phase 2 |
| Dependency and code scanning, SARIF | Phase 2 |
| Path filters, data-triggered pipelines | Phase 3 |
| ML quality gates, baselines | Phase 4 |
| Test doubles for pipeline speed, contract tests | Phase 5 |
| Scheduled workflows, `workflow_dispatch` inputs, PR comments, Pages | Phase 6 |
| Environments, approvals, OIDC, signing, SBOMs | Phase 8 |
| Self-hosted runners and their security model | Phase 8 |
| Deployment verification and rollback | Phase 8 |
| DORA metrics | Phase 8 |

---

## 45. Immediate Next Milestone

Create the Python project and complete **Phase 0 — Walking skeleton**:

```text
uv project + FastAPI /health/live + one test + Makefile + pre-commit + ci.yml + branch protection
```

Then Phase 1 (Incident API + PostgreSQL + Testcontainers in CI). Only after the backend and its pipeline are clean should AI/RAG functionality be added.

This keeps the project valuable for:

```text
AI/ML and MLOps roles
and
Python backend / platform roles
```
