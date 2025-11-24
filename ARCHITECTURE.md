# Architecture Documentation

## Project Structure

### Core Application Files

#### 1. `main.py` - FastAPI Application
**Purpose**: Main entry point for the API server

**Key Features**:
- FastAPI application initialization
- API endpoint definitions (`/health`, `/api/v1/conversations`, `/api/v1/insights`)
- Rate limiting integration
- Database session management
- Batch processor lifecycle management

**Endpoints**:

1. **POST /api/v1/conversations**
   - Accepts conversation data and stores in database
   - Rate limiting check (100 req/s)
   - Returns 202 Accepted when queued successfully
   - Returns 429 Too Many Requests when rate limit exceeded
   - Returns 400 Bad Request for invalid schema

2. **GET /api/v1/insights**
   - Retrieves analyzed insights
   - Supports filtering by time range, confidence, and sentiment
   - Pagination support (max limit: 1000)

---

#### 2. `models.py` - Database Models
**Purpose**: SQLAlchemy ORM schema definitions

**Models**:

1. **Conversation Table**
   - `id`: Unique identifier (format: conv_xxxxx)
   - `text`: Conversation content
   - `author`: Author/username
   - `timestamp`: Conversation timestamp
   - `raw_data`: Original data (JSON)
   - `status`: Processing status (pending, processing, completed, failed)
   - Indexes: timestamp, status for fast queries

2. **Insight Table**
   - `conversation_id`: Links to Conversation
   - `sentiment_score`: Sentiment score (-1.0 to 1.0)
   - `clusters`: Topic clusters array (JSON)
   - `confidence`: Analysis confidence (0.0 to 1.0)
   - `reasoning`: Analysis reasoning
   - `grok_analysis`: Full Grok response (for debugging)
   - Indexes: conversation_id, timestamp, sentiment_score, confidence

---

#### 3. `schemas.py` - Pydantic Schemas
**Purpose**: Request/response data validation and serialization

**Schemas**:
- `ConversationRequest`: Input validation for conversation submission
- `ConversationResponse`: 202 Accepted response format
- `InsightsResponse`: Insights retrieval response
- `ErrorResponse`: Error response format

---

#### 4. `database.py` - Database Connection
**Purpose**: Database connection pool and session management

**Features**:
- Async SQLite connection
- Session factory creation
- Database initialization (table creation)

---

#### 5. `grok_client.py` - Grok API Client
**Purpose**: Communication with Grok API for analysis

**Key Features**:

1. **Rate Limiting (10 calls/s)**
   - Semaphore-based concurrent call limiting
   - Time window-based throttling
   - Automatic wait handling

2. **Sentiment Analysis & Topic Clustering**
   - Structured prompt engineering
   - JSON response parsing
   - Markdown code block removal

3. **Error Handling**
   - Exponential backoff retry logic
   - 429 Rate Limit handling
   - Fallback for JSON parsing failures

---

#### 6. `rate_limiter.py` - Rate Limiting
**Purpose**: API endpoint request limiting

**Implementation**: Token Bucket algorithm
- Maximum requests per time window
- Returns False when rate limit exceeded
- Calculates Retry-After header

---

#### 7. `batch_processor.py` - Batch Processing System
**Purpose**: Background processing of conversations using Grok API

**Key Features**:

1. **Async Batch Processing**
   - Checks for pending conversations every 5 seconds
   - Processes in batches of 10
   - Parallel processing (within Grok rate limits)

2. **Status Management**
   - pending → processing → completed/failed
   - Tracks status at each stage

3. **Error Handling**
   - Individual conversation failures don't stop batch
   - Failed conversations are marked with status

---

#### 8. `ingest_data.py` - Data Ingestion Script
**Purpose**: Load test data or Kaggle dataset into API

**Features**:
- Sample conversation data (10 examples)
- CSV file reading (Kaggle dataset format)
- Bulk data submission via API
- Parallel processing for fast ingestion

---

## Data Flow

### Conversation Submission Flow
```
Client → POST /api/v1/conversations
  ↓
Rate Limiter Check (100 req/s)
  ↓
Data Validation (Pydantic)
  ↓
Save to Database (status: pending)
  ↓
202 Accepted Response
  ↓
[Background] Batch Processor detects
  ↓
Grok API Call (Rate limit: 10 calls/s)
  ↓
Save Insight (status: completed)
```

### Insights Retrieval Flow
```
Client → GET /api/v1/insights?start_time=...&end_time=...
  ↓
Query Parameter Validation
  ↓
Database Query with Filters
  ↓
JSON Response
```

## Design Decisions

### 1. SQLite over PostgreSQL
- **Reason**: Resource constraints (1GB RAM)
- **Benefit**: Lightweight, no setup required, single-server friendly

### 2. Async Processing
- **Reason**: Leverage FastAPI's async capabilities
- **Benefit**: Better concurrent performance, minimize Grok API wait time

### 3. Batch Processing over Immediate
- **Reason**: Improve API response time
- **Benefit**: Efficient Grok API usage, better scalability

### 4. Custom Rate Limiter
- **Reason**: More fine-grained control
- **Benefit**: Exactly matches requirements, educational purpose

## Resource Constraints

The application is optimized to run within:
- **CPU**: 2 cores
- **Memory**: 1GB RAM
- **Storage**: 10GB

## Technology Stack

- **Framework**: FastAPI
- **Database**: SQLite (via aiosqlite)
- **ORM**: SQLAlchemy (async)
- **API Client**: httpx (async)
- **Validation**: Pydantic
- **Containerization**: Docker

