# AI Customer Support Agent

A production-oriented AI agent (not a chatbot) that reasons about a user's
request, selects and chains tools, uses RAG only where relevant, and
maintains multi-turn state — built with LangGraph on top of FastAPI.

Follow-on project to [QueryForge](https://github.com/GyanBiswal/queryforge)
(production RAG platform). RAG here is one tool among several rather than
the center of the system.

## Status
Phase 1 (architecture) complete. Scaffolding in progress.

## Architecture decisions (locked)

- **Agent state**: explicit typed fields (`messages`, `pending_tool_calls`,
  `tool_results`, `next_action`) rather than a messages-only state, so graph
  routing is deterministic and testable instead of parsing LLM text.
- **Tool selection**: native LLM tool-calling (Groq function calling) proposes
  actions; a Python-side validation/execution layer in the `tool_executor`
  node actually performs them. LLM orchestrates, code executes — business
  logic never lives in prompts.
- **Single database**: PostgreSQL + pgvector for both relational data (orders,
  refunds, tickets, conversation history) and vector search (FAQ/RAG),
  instead of a second dedicated vector store — fewer moving parts,
  transactional consistency.
- **Redis's scope**: LangGraph checkpointing + ephemeral session state only.
  Postgres remains the system of record for anything durable.

## Stack

| Layer | Choice |
|---|---|
| API | FastAPI |
| Agent framework | LangGraph |
| LLM | Groq (free tier) |
| Embeddings | local open-source model |
| Database | PostgreSQL + pgvector |
| Cache / checkpointing | Redis |
| Auth | JWT |
| ORM | SQLAlchemy (async) |
| Migrations | Alembic |
| Frontend | Next.js |
| Deployment | Docker Compose |

## Project structure

\`\`\`
app/
  api/            # FastAPI routes — no business logic here
  agent/
    nodes/        # LangGraph graph nodes (plan, tool_executor, respond, ...)
    tools/         # Tool definitions (schema + dispatch)
  rag/            # Retrieval logic, exposed as a tool
  services/       # Business logic
  repositories/   # DB access layer
  db/
    models/       # SQLAlchemy models
    migrations/   # Alembic
  auth/           # JWT auth
  llm_providers/  # Swappable LLM provider interface (Groq, etc.)
  schemas/        # Pydantic request/response + tool schemas
  core/           # Config, logging, exceptions
  tests/
frontend/         # Next.js app
docs/             # Architecture docs, diagrams, ADRs
\`\`\`

## Setup
_Coming in the scaffolding phase — Docker Compose (Postgres+pgvector, Redis,
API), \`.env\` config, and local dev instructions will land here._