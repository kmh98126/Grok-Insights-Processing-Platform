# Insights Platform API — Project Portfolio

> **Insights Platform API** | FastAPI + Grok AI | Twitter Conversation Analysis Platform

---

## Table of Contents

| # | Section | Description |
|---|---------|-------------|
| 01 | [Project Overview](#01-project-overview) | Project summary and objectives |
| 02 | [Key Features](#02-key-features) | Core features and capabilities |
| 03 | [System Architecture](#03-system-architecture) | Architecture and data flow design |
| 04 | [Technology Stack](#04-technology-stack) | Frameworks and libraries used |
| 05 | [API Design](#05-api-design) | RESTful API endpoint specifications |
| 06 | [Database Design](#06-database-design) | Data models and schema design |
| 07 | [Core Components](#07-core-components) | Detailed component breakdown |
| 08 | [Rate Limiting & Performance](#08-rate-limiting--performance) | Performance optimization strategies |
| 09 | [Deployment](#09-deployment) | Docker containerization and deployment |
| 10 | [Project Structure](#10-project-structure) | File and directory organization |
| 11 | [Challenges & Solutions](#11-challenges--solutions) | Technical decisions and problem-solving |

---

## 01. Project Overview

### Introduction

Insights Platform API is a production-ready backend system designed for real-time analysis of Twitter conversations using xAI's Grok AI model. The platform receives raw conversation data through a RESTful API, processes it asynchronously using AI-powered sentiment analysis and topic clustering, and provides structured insights through queryable endpoints.

### Project Objectives

- Build a high-performance async API capable of handling 100+ requests/second
- Integrate Grok AI for intelligent sentiment analysis and topic categorization
- Implement robust rate limiting to manage both inbound traffic and external API calls
- Design an efficient background batch processing system for scalable data analysis
- Create a containerized deployment with strict resource constraints (2 CPU, 1GB RAM)
- Provide filtered and paginated insight retrieval with confidence-based scoring

### Use Case Scenario

A customer service platform collects thousands of Twitter conversations daily. The Insights Platform API ingests this data, analyzes each conversation for sentiment polarity (-1.0 to +1.0), identifies topic clusters (e.g., `delivery_problems`, `product_issues`, `praise`), and assigns a confidence score. Support teams can then query insights filtered by time range, sentiment type, and confidence threshold to prioritize responses and identify emerging trends.

### Key Metrics

| Metric | Value |
|--------|-------|
| API Framework | FastAPI (Python 3.11+) |
| AI Engine | Grok AI (xAI) |
| Database | SQLite (async via aiosqlite) |
| Inbound Rate Limit | 100 requests/second |
| Grok API Rate Limit | 10 calls/second |
| Batch Size | 10 conversations per cycle |
| Max Query Results | 1,000 per request |
| Deployment | Docker (2 CPU, 1GB RAM) |

---

## 02. Key Features

### 2.1 RESTful API Design

Clean, well-documented REST API built with FastAPI. Supports conversation submission (POST) and insight retrieval (GET) with comprehensive request validation using Pydantic models. Follows HTTP semantics with proper status codes (202 Accepted, 429 Too Many Requests, 400 Bad Request).

### 2.2 Grok AI Integration

Deep integration with xAI's Grok model for advanced NLP analysis. Each conversation is analyzed for:

- **Sentiment polarity** — score from -1.0 to 1.0
- **Topic clustering** — identifying categories like `product_issues`, `delivery_problems`, `praise`
- **Confidence scoring** — how certain the AI is about the analysis

Structured prompt engineering ensures consistent JSON output from the AI model.

### 2.3 Asynchronous Batch Processing

Background batch processor that polls for pending conversations every 5 seconds, processes them in batches of 10 with parallel execution, and manages status transitions (`pending` → `processing` → `completed`/`failed`). Individual failures don't affect the batch, ensuring resilience.

### 2.4 Dual Rate Limiting

Two-tier rate limiting system:

- **Inbound API traffic** — limited to 100 requests/second using a token bucket algorithm with sliding window
- **Outbound Grok API calls** — throttled to 10 calls/second using semaphore-based concurrency control with time-window tracking

### 2.5 Advanced Query Filtering

Insight retrieval supports powerful filtering:

- Time range queries (ISO8601)
- Sentiment type filtering (positive / negative / neutral)
- Minimum confidence thresholds (0.0–1.0)
- Pagination with configurable limits (up to 1,000 results)
- Results ordered by timestamp descending

### 2.6 Docker Containerization

Production-ready Docker setup with multi-stage build, resource constraints (2 CPU cores, 1GB RAM, 512MB reserved), persistent database volume mounting, and Docker Compose orchestration. Optimized for lightweight deployment on constrained infrastructure.

---

## 03. System Architecture

### Architecture Overview

The system follows an event-driven, asynchronous architecture pattern. Conversations are submitted through the REST API and immediately stored with a `pending` status. A background batch processor continuously polls for unprocessed conversations, sends them to Grok AI for analysis, and stores the structured insights back in the database. This decoupled design ensures fast API response times (202 Accepted) while handling AI processing asynchronously.

### Data Flow — Conversation Submission

```
Client
  │
  ▼
POST /api/v1/conversations
  │
  ▼
Rate Limiter ──── 100 req/s check ──── [429 Reject]
  │
  ▼ (allowed)
Pydantic Schema ──── Validate request body
  │
  ▼
SQLAlchemy ORM ──── Insert to conversations table (status: pending)
  │
  ▼
FastAPI ──── Return 202 Accepted + conversation_id
```

| Step | Component | Action | Output |
|------|-----------|--------|--------|
| 1 | Client | POST /api/v1/conversations | HTTP Request |
| 2 | Rate Limiter | Token bucket check (100 req/s) | Allow / 429 Reject |
| 3 | Pydantic Schema | Validate request body | ConversationRequest |
| 4 | SQLAlchemy ORM | Insert to conversations table | status: pending |
| 5 | FastAPI | Return response | 202 Accepted + conv_id |

### Data Flow — Background Processing

```
Batch Processor
  │
  ▼
Poll DB every 5 seconds ──── SELECT * WHERE status = 'pending' LIMIT 10
  │
  ▼
Update status to 'processing'
  │
  ▼
Grok Client ──── Send to Grok API (10 calls/s rate limit)
  │
  ▼
Parse & validate JSON response
  │
  ▼
Insert Insight record + Update conversation status to 'completed'
```

| Step | Component | Action | Output |
|------|-----------|--------|--------|
| 1 | Batch Processor | Poll DB every 5 seconds | Pending conversations |
| 2 | Batch Processor | Update status to processing | Batch of 10 |
| 3 | Grok Client | Send to Grok API (10 calls/s) | AI Analysis JSON |
| 4 | Grok Client | Parse & validate response | Structured insight data |
| 5 | SQLAlchemy ORM | Insert insight + update status | status: completed |

### Data Flow — Insights Retrieval

```
Client
  │
  ▼
GET /api/v1/insights?start_time=...&end_time=...&sentiment=...
  │
  ▼
FastAPI ──── Parse & validate query params
  │
  ▼
SQLAlchemy ORM ──── Build filtered query (WHERE + indexes)
  │
  ▼
Database ──── Execute query
  │
  ▼
FastAPI ──── Serialize to InsightsResponse JSON + metadata
```

| Step | Component | Action | Output |
|------|-----------|--------|--------|
| 1 | Client | GET /api/v1/insights?params | HTTP Request |
| 2 | FastAPI | Parse & validate query params | Typed parameters |
| 3 | SQLAlchemy ORM | Build filtered query | SQL with WHERE clauses |
| 4 | Database | Execute with indexes | Insight records |
| 5 | FastAPI | Serialize to JSON | InsightsResponse + metadata |

### Design Principles

- **Separation of Concerns** — API handling, data persistence, AI processing, and rate limiting are isolated into dedicated modules (`main.py`, `models.py`, `grok_client.py`, `rate_limiter.py`).
- **Async-First Design** — Every I/O operation uses async/await, from database queries (aiosqlite) to HTTP calls (httpx), maximizing throughput on limited CPU resources.
- **Graceful Degradation** — Individual conversation processing failures are isolated; the batch processor continues with remaining items. JSON parsing failures fall back to default values.
- **Resource Awareness** — SQLite chosen over PostgreSQL to minimize memory footprint. Batch sizes and concurrency limits are tuned for the 2-core, 1GB RAM constraint.

---

## 04. Technology Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| Web Framework | FastAPI | 0.121.3 | High-performance async API framework with auto-generated docs |
| ASGI Server | Uvicorn | 0.38.0 | Lightning-fast ASGI server for production deployment |
| Validation | Pydantic | 2.12.4 | Data validation and serialization with type hints |
| ORM | SQLAlchemy | 2.0.36 | Async ORM for database operations with 2.0 style |
| Database | SQLite + aiosqlite | 0.20.0 | Lightweight async database for resource-constrained environments |
| HTTP Client | httpx | 0.27.2 | Modern async HTTP client for Grok API communication |
| Rate Limiting | Custom + slowapi | 0.1.9 | Token bucket and semaphore-based rate control |
| Containerization | Docker | 3.8 | Containerized deployment with resource limits |
| Language | Python | 3.11+ | Modern Python with async/await native support |

### Why FastAPI?

FastAPI was chosen for several critical reasons: native async/await support for high-concurrency workloads, automatic OpenAPI documentation generation, Pydantic integration for request/response validation, dependency injection system for clean database session management, and exceptional performance benchmarks that rival Node.js and Go frameworks. Its type-hint-driven development approach also reduces bugs and improves code maintainability.

### Why SQLite over PostgreSQL?

Given the resource constraints of 1GB RAM, SQLite was selected over PostgreSQL for several reasons: zero configuration and no separate server process required, minimal memory footprint (operates within the application process), sufficient performance for the expected workload, and simplified deployment with Docker volume mounting. The async wrapper (aiosqlite) ensures non-blocking I/O despite SQLite's inherently synchronous nature.

### Why Grok AI?

xAI's Grok model provides state-of-the-art natural language understanding with a focus on Twitter/X platform content. Its API follows the OpenAI-compatible chat completions format, making it straightforward to integrate. The model excels at understanding social media language patterns, informal text, and context-dependent sentiment, which is critical for accurate Twitter conversation analysis.

---

## 05. API Design

The API follows RESTful design principles with clear resource naming, proper HTTP method usage, appropriate status codes, and consistent error response formats.

### Endpoint: `POST /api/v1/conversations`

Submits a new conversation for AI-powered analysis. Returns immediately with `202 Accepted` status, indicating the conversation has been queued for background processing.

**Request Body:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `text` | string | Yes | Conversation text content (min 1 char) |
| `author` | string | No | Author username or identifier |
| `timestamp` | ISO8601 datetime | No | Conversation timestamp (defaults to now) |
| `raw_data` | object | No | Additional metadata (stored as JSON) |

**Example Request:**

```json
{
  "text": "Still waiting on my order...",
  "author": "customer123",
  "timestamp": "2025-01-20T10:00:00Z",
  "raw_data": {}
}
```

**Response Codes:**

| Status Code | Condition | Response Body |
|-------------|-----------|---------------|
| `202 Accepted` | Success | `{"status": "accepted", "conversation_id": "conv_a1b2c3d4", "message": "Conversation queued for analysis"}` |
| `429 Too Many Requests` | Rate limit exceeded | `{"error": "rate_limit_exceeded", "retry_after": 5}` |
| `400 Bad Request` | Invalid schema | `{"error": "invalid_schema", "details": "Missing required field: text"}` |

---

### Endpoint: `GET /api/v1/insights`

Retrieves analyzed insights with powerful filtering capabilities. Supports time-range queries, sentiment filtering, confidence thresholds, and pagination.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `start_time` | ISO8601 datetime | Yes | Start of time range filter |
| `end_time` | ISO8601 datetime | Yes | End of time range filter |
| `limit` | integer (1–1000) | No | Maximum results to return (default: 100) |
| `min_confidence` | float (0.0–1.0) | No | Minimum confidence score threshold |
| `sentiment` | enum | No | Filter: `positive` / `negative` / `neutral` |

**Example Request:**

```
GET /api/v1/insights?start_time=2025-01-20T00:00:00Z&end_time=2025-01-21T00:00:00Z&limit=100&sentiment=negative
```

**Example Response:**

```json
{
  "insights": [
    {
      "conversation_id": "conv_a1b2c3d4",
      "timestamp": "2025-01-20T10:00:00Z",
      "text": "Still waiting on my order...",
      "grok_analysis": {
        "sentiment_score": -0.65,
        "clusters": ["delivery_problems"],
        "confidence": 0.90,
        "reasoning": "Negative sentiment regarding delivery delays"
      }
    }
  ],
  "metadata": {
    "total_count": 523,
    "returned_count": 100,
    "start_time": "2025-01-20T00:00:00Z",
    "end_time": "2025-01-21T00:00:00Z"
  }
}
```

---

### Endpoint: `GET /health`

Simple health check endpoint returning `{"status": "ok"}`. Used for Docker health checks, load balancer probes, and monitoring systems.

---

## 06. Database Design

The database uses two core tables with a one-to-one relationship between conversations and their analysis results. Strategic indexing ensures fast queries even as data grows.

### Conversations Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | String (PK) | Auto-generated | Format: `conv_{uuid8}` (e.g., `conv_a1b2c3d4`) |
| `text` | String | NOT NULL | Raw conversation text content |
| `author` | String | Nullable | Author username or identifier |
| `timestamp` | DateTime | NOT NULL, Indexed | Conversation timestamp |
| `raw_data` | JSON | Nullable | Original metadata stored as JSON |
| `status` | String | Indexed | `pending` \| `processing` \| `completed` \| `failed` |
| `created_at` | DateTime | Auto-set | Record creation timestamp |

> **Indexes:** `idx_conv_timestamp` (timestamp), `idx_conv_status` (status)

### Insights Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | Integer (PK) | Auto-increment | Sequential primary key |
| `conversation_id` | String (FK) | NOT NULL, Indexed | References `conversations.id` |
| `timestamp` | DateTime | NOT NULL, Indexed | Original conversation timestamp |
| `text` | String | NOT NULL | Conversation text (denormalized for fast access) |
| `sentiment_score` | Float | Indexed | Sentiment polarity: -1.0 to +1.0 |
| `clusters` | JSON | Nullable | Topic categories array (e.g., `["praise", "product"]`) |
| `confidence` | Float | Indexed | Analysis confidence: 0.0 to 1.0 |
| `reasoning` | String | Nullable | AI explanation of the analysis |
| `grok_analysis` | JSON | Nullable | Full Grok API response (for debugging) |
| `created_at` | DateTime | Auto-set | Record creation timestamp |

> **Indexes:** `idx_insight_conversation_id`, `idx_insight_timestamp`, `idx_insight_sentiment`, `idx_insight_confidence`

### Indexing Strategy

Strategic indexing is applied to columns frequently used in WHERE clauses and JOIN conditions:

- **conversations.status** — Efficient batch processor polling (`WHERE status = 'pending'`)
- **conversations.timestamp** — Time-range queries
- **insights.conversation_id** — Relationship lookups
- **insights.timestamp** — Range queries for insight retrieval
- **insights.sentiment_score** — Sentiment filtering (`> 0.1` for positive, `< -0.1` for negative)
- **insights.confidence** — Threshold filtering (`>= min_confidence`)

---

## 07. Core Components

### 7.1 `main.py` — FastAPI Application

**248 lines**

The application entry point that initializes FastAPI, defines all API endpoints, manages the application lifecycle (startup/shutdown events), and coordinates between rate limiting, database, and batch processing components. Uses FastAPI's dependency injection for database session management and implements comprehensive error handling with proper HTTP status codes.

**Key Implementation Details:**

- Lifecycle management: Database initialization and batch processor start/stop via `@app.on_event("startup")` and `@app.on_event("shutdown")`
- Rate limiting integration at the endpoint level — checks `inbound_limiter.acquire()` before processing
- Pydantic model-based request/response validation with `response_model` parameter
- Dynamic query building with SQLAlchemy for filtered insights retrieval (time range, sentiment, confidence)
- Comprehensive error handling with database rollback support on failures

---

### 7.2 `grok_client.py` — Grok AI Client

**139 lines**

Handles all communication with xAI's Grok API. Implements structured prompt engineering for consistent JSON output, semaphore-based rate limiting (10 calls/second), retry logic with exponential backoff, and robust response parsing that handles markdown code block wrapping from the AI model.

**Key Implementation Details:**

- Structured prompt engineering for sentiment analysis and topic clustering — instructs Grok to return strict JSON format
- Semaphore + sliding window rate limiting (10 calls/second) using `asyncio.Semaphore(10)` and timestamp tracking
- Markdown code block stripping — removes ` ```json ` and ` ``` ` wrappers from Grok responses before parsing
- Exponential backoff retry (3 attempts) for transient failures — `2^attempt` seconds between retries
- Graceful fallback with default values on JSON parsing errors — returns `sentiment_score=0.0`, `confidence=0.0`, `clusters=["unknown"]`
- 429 rate limit response handling with `Retry-After` header support

---

### 7.3 `batch_processor.py` — Background Processor

**115 lines**

An asyncio-based background task that continuously processes pending conversations. Uses `asyncio.create_task` for non-blocking execution, `asyncio.gather` for parallel batch processing, and proper status state machine management.

**Key Implementation Details:**

- Polling loop: checks for pending conversations every 5 seconds
- Batch processing: 10 conversations per cycle with parallel execution via `asyncio.gather`
- Status state machine: `pending` → `processing` → `completed` / `failed`
- Error isolation: individual failures don't affect the batch — each conversation is wrapped in try/except
- Graceful shutdown with task cancellation support via `asyncio.CancelledError`

---

### 7.4 `rate_limiter.py` — Rate Limiting Engine

**57 lines**

Implements a token bucket algorithm with sliding window for precise rate limiting. Uses `asyncio.Lock` for thread-safe token management and `deque` for efficient time-window tracking. Provides `Retry-After` calculation for 429 responses.

**Key Implementation Details:**

- Token bucket algorithm with sliding time window using `collections.deque`
- Async lock (`asyncio.Lock`) for safe concurrent access
- Configurable `max_requests` and `time_window` parameters
- `get_retry_after()` method for calculating Retry-After header value
- Global `inbound_limiter` instance configured at 100 req/s

---

### 7.5 `models.py` — Database Models

**55 lines**

SQLAlchemy 2.0 declarative models defining the database schema. Uses Column definitions with proper types, constraints, and strategic indexes for query performance.

**Key Implementation Details:**

- UUID-based conversation IDs using `conv_{uuid.uuid4().hex[:8]}` format
- JSON columns (`raw_data`, `clusters`, `grok_analysis`) for flexible metadata storage
- Strategic composite indexes on frequently queried columns (`timestamp`, `status`, `sentiment_score`, `confidence`)
- Default value generators using lambda functions for timestamps and IDs

---

### 7.6 `schemas.py` — Pydantic Schemas

**66 lines**

Request/response validation schemas using Pydantic v2. Defines strict type validation, value ranges, and custom validators. Supports ORM mode for direct model serialization.

**Key Implementation Details:**

- `ConversationRequest` with custom `@validator('text')` — ensures text is non-empty and trimmed
- `GrokAnalysis` with bounded float fields — `sentiment_score` constrained to [-1.0, 1.0], `confidence` to [0.0, 1.0]
- `SentimentFilter` enum for type-safe query parameters (`positive`, `negative`, `neutral`)
- `InsightItem` with `from_attributes = True` config for ORM compatibility
- `ErrorResponse` with optional `retry_after` field for rate limit responses

---

## 08. Rate Limiting & Performance

The system implements a dual-layer rate limiting strategy to protect both the API server and the external Grok AI service from overload.

### Inbound Rate Limiter (Token Bucket)

The inbound rate limiter uses a **token bucket algorithm** with a sliding time window. It maintains a deque of request timestamps and removes entries older than the configured time window (1 second). If the deque length equals the max capacity (100), the request is rejected with a 429 status code and a calculated Retry-After header.

| Parameter | Value | Description |
|-----------|-------|-------------|
| Algorithm | Token Bucket | Sliding window with timestamp deque |
| Max Requests | 100 / second | Maximum inbound API requests |
| Time Window | 1.0 second | Sliding window duration |
| Concurrency | `asyncio.Lock` | Thread-safe async access |
| Rejection | HTTP 429 | Includes Retry-After header |

### Grok API Rate Limiter (Semaphore + Window)

The Grok API rate limiter combines an **`asyncio.Semaphore`** (limiting to 10 concurrent calls) with a **time-window tracker** that maintains a list of recent call timestamps. If 10 calls have been made within the last second, the system calculates the precise wait time and sleeps before proceeding. This dual approach prevents both burst overload and sustained rate violation.

| Parameter | Value | Description |
|-----------|-------|-------------|
| Concurrency Limit | 10 simultaneous | `asyncio.Semaphore(10)` |
| Rate Limit | 10 calls / second | Time-window based throttling |
| Call Interval | 100ms minimum | Effective spacing between calls |
| Retry Strategy | Exponential backoff | `2^attempt` seconds (max 3 retries) |
| 429 Handling | Retry-After header | Respects server-specified wait time |

### Performance Optimization Strategies

- **Async I/O Everywhere** — All database operations use async SQLAlchemy with aiosqlite. All HTTP calls use async httpx. This maximizes CPU utilization during I/O wait times.
- **Batch Processing** — Instead of processing each conversation immediately, the system batches 10 at a time and processes them in parallel using `asyncio.gather`, reducing overhead.
- **Database Indexing** — Strategic indexes on `timestamp`, `status`, `sentiment_score`, and `confidence` columns ensure O(log n) query performance for filtered insight retrieval.
- **Connection Pooling** — SQLAlchemy's async engine manages a connection pool, avoiding the overhead of creating new database connections for each request.
- **Lightweight Stack** — SQLite eliminates the overhead of a separate database server process, keeping the total memory footprint well within the 1GB constraint.
- **Low-Temperature AI Calls** — Grok API calls use `temperature=0.3` for more deterministic, consistent analysis results, reducing the need for retries due to inconsistent output.

---

## 09. Deployment

The application is containerized with Docker for consistent deployment across environments. Docker Compose provides orchestration with resource constraints matching production requirements.

### Dockerfile Configuration

| Stage | Command | Purpose |
|-------|---------|---------|
| Base Image | `FROM python:3.11-slim` | Minimal Python image for small footprint |
| System Deps | `apt-get install gcc` | C compiler for native Python extensions |
| Dependencies | `pip install -r requirements.txt` | Install Python packages (cached layer) |
| Application | `COPY . .` | Copy application source code |
| Expose | `EXPOSE 8000` | Declare API port |
| Run | `uvicorn main:app --host 0.0.0.0 --port 8000` | Start ASGI server |

### Docker Compose — Resource Constraints

| Resource | Limit | Reservation | Notes |
|----------|-------|-------------|-------|
| CPU | 2 cores | 1 core | Sufficient for async workload + batch processing |
| Memory | 1 GB | 512 MB | SQLite in-process, no separate DB server |
| Storage | 10 GB | — | Database file + application code |
| Port | 8000:8000 | — | Host-to-container port mapping |
| Restart | unless-stopped | — | Auto-restart on crash |

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROK_KEY` | Yes | — | xAI Grok API authentication key |
| `DATABASE_URL` | No | `sqlite+aiosqlite:///./insights.db` | Database connection string |
| `API_URL` | No | `http://localhost:8000` | Base URL for data ingestion script |

### Quick Start Commands

```bash
# Build and run with Docker
docker build -t insights-platform .
docker run -d -p 8000:8000 -e GROK_KEY="your-key" --name insights-platform insights-platform

# Or with Docker Compose
docker-compose up -d

# Health check
curl http://localhost:8000/health

# Local development
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
export GROK_KEY="your-key"
uvicorn main:app --reload
```

---

## 10. Project Structure

The project follows a flat, modular structure where each file has a single, well-defined responsibility. This design simplifies navigation and testing.

### File Overview

| File | Lines | Category | Responsibility |
|------|-------|----------|----------------|
| `main.py` | 248 | Application | FastAPI app, endpoints, lifecycle management |
| `models.py` | 55 | Data Layer | SQLAlchemy ORM models (Conversation, Insight) |
| `schemas.py` | 66 | Validation | Pydantic request/response schemas |
| `database.py` | 37 | Data Layer | Async engine, session factory, initialization |
| `grok_client.py` | 139 | AI Integration | Grok API client, prompt engineering, rate limiting |
| `rate_limiter.py` | 57 | Middleware | Token bucket rate limiter implementation |
| `batch_processor.py` | 115 | Processing | Background batch processing system |
| `ingest_data.py` | ~100 | Utility | Data ingestion script (sample + CSV) |
| `requirements.txt` | 16 | Config | Python dependency declarations |
| `Dockerfile` | 24 | DevOps | Container image build instructions |
| `docker-compose.yml` | 24 | DevOps | Container orchestration with resource limits |
| `test_api.sh` | ~50 | Testing | Shell-based API endpoint tests |
| `README.md` | 241 | Docs | Setup, API docs, usage, troubleshooting |
| `ARCHITECTURE.md` | 208 | Docs | Architecture documentation and design decisions |
| `TESTING.md` | — | Docs | Testing guide with scenarios and checklist |

> **Total:** ~8 Python source files, ~720+ lines of application code, 3 documentation files, 3 config/DevOps files

### Module Dependency Graph

```
main.py
├── database.py ──── models.py
├── models.py
├── schemas.py
├── rate_limiter.py
└── batch_processor.py
    ├── models.py
    ├── grok_client.py  ──── (httpx, asyncio)
    └── database.py
```

| Module | Depends On |
|--------|------------|
| `main.py` | database, models, schemas, rate_limiter, batch_processor |
| `batch_processor.py` | models, grok_client, database |
| `grok_client.py` | (external: httpx, asyncio) |
| `rate_limiter.py` | (standalone: asyncio, collections) |
| `models.py` | (standalone: SQLAlchemy) |
| `schemas.py` | (standalone: Pydantic) |
| `database.py` | models |

---

## 11. Challenges & Solutions

### Challenge 1: Grok API Response Inconsistency

**Problem:** Grok AI sometimes wraps JSON responses in markdown code blocks (` ```json...``` `) and occasionally returns malformed JSON, causing parsing failures.

**Solution:** Implemented a robust response parser that strips markdown code block wrappers before JSON parsing. Added a 3-retry mechanism with exponential backoff (1s, 2s, 4s) and a graceful fallback that returns default values (`sentiment_score=0.0`, `confidence=0.0`, `clusters=["unknown"]`) when all retries fail.

---

### Challenge 2: Dual Rate Limiting Coordination

**Problem:** Needed to limit inbound API traffic (100 req/s) and outbound Grok calls (10 calls/s) with different strategies, while keeping the system responsive.

**Solution:** Implemented two separate rate limiting mechanisms: a token bucket algorithm with `asyncio.Lock` for inbound traffic (synchronous check on each request), and a semaphore + time-window tracker for Grok API calls (asynchronous wait with precise sleep calculation). The separation ensures neither limiter blocks the other.

---

### Challenge 3: Resource-Constrained Deployment

**Problem:** The application must run within 2 CPU cores and 1GB RAM, ruling out heavy database servers like PostgreSQL and limiting concurrency options.

**Solution:** Selected SQLite with async wrapper (aiosqlite) to eliminate separate database process overhead. Tuned batch sizes to 10 conversations and Grok concurrency to 10 calls to balance throughput with memory usage. Used Python 3.11-slim Docker image to minimize container size.

---

### Challenge 4: Asynchronous Background Processing

**Problem:** Background batch processing must run continuously without blocking API request handling, while sharing the same database and respecting rate limits.

**Solution:** Used `asyncio.create_task` to spawn the batch processor as a non-blocking background task. Each batch creates its own database session (`AsyncSessionLocal`) to avoid session conflicts. The processor uses `asyncio.gather` for parallel conversation processing within each batch, and individual failures are caught without affecting other conversations in the batch.

---

### Challenge 5: Graceful Error Isolation

**Problem:** A single Grok API failure or malformed response could potentially crash the entire batch processing pipeline, leaving conversations in a stuck state.

**Solution:** Implemented per-conversation error handling within `_process_single`. Failed conversations are marked with `status="failed"` while the batch continues. The batch processor's main loop also catches exceptions at the batch level and waits 5 seconds before retrying. This multi-level error handling ensures the system remains operational even under partial failure conditions.

---

## Summary

The Insights Platform API demonstrates a production-grade approach to building AI-powered data analysis pipelines. By combining FastAPI's async capabilities with Grok AI's NLP power, the system achieves high throughput within strict resource constraints. The modular architecture, comprehensive error handling, and dual rate limiting strategy make it resilient and maintainable.

**Skills demonstrated in this project:**

- RESTful API design and implementation
- Asynchronous programming with Python asyncio
- AI/LLM integration and prompt engineering
- Database schema design and query optimization
- Rate limiting algorithms (token bucket, semaphore)
- Docker containerization and resource management
- Error handling and graceful degradation patterns
