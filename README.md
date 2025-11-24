# Insights Platform API

A FastAPI-based backend API for analyzing Twitter conversations using Grok AI. This platform processes conversation data to generate insights such as sentiment analysis and topic clustering.

## Features

- **RESTful API** for submitting and retrieving conversation insights
- **Grok AI Integration** for sentiment analysis and topic clustering
- **Asynchronous Processing** with background batch processing
- **Rate Limiting** (100 req/s inbound, 10 calls/s to Grok)
- **SQLite Database** for efficient storage
- **Docker Support** for easy deployment

## Prerequisites

- Python 3.11+
- Docker and Docker Desktop
- Grok API key (use promo code `grok_eng_5aef7b52` on console.x.ai)

## Quick Start

### Using Docker (Recommended)

1. **Build the Docker image:**
   ```bash
   docker build -t insights-platform .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 8000:8000 \
     -e GROK_KEY="your-api-key-here" \
     --name insights-platform \
     insights-platform
   ```

3. **Check if the server is running:**
   ```bash
   curl http://localhost:8000/health
   ```

### Local Development

1. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variable:**
   ```bash
   export GROK_KEY="your-api-key-here"
   ```

4. **Run the application:**
   ```bash
   uvicorn main:app --reload
   ```

## API Endpoints

### Health Check
- **GET** `/health`
- Returns: `{"status": "ok"}`

### Submit Conversation
- **POST** `/api/v1/conversations`
- **Request body:**
  ```json
  {
    "text": "Still waiting on my order...",
    "author": "customer123",
    "timestamp": "2025-01-20T10:00:00Z",
    "raw_data": {}
  }
  ```
- **Responses:**
  - `202 Accepted`: Conversation queued for processing
    ```json
    {
      "status": "accepted",
      "conversation_id": "conv_a1b2c3d4",
      "message": "Conversation queued for analysis"
    }
    ```
  - `429 Too Many Requests`: Rate limit exceeded
    ```json
    {
      "error": "rate_limit_exceeded",
      "retry_after": 5
    }
    ```
  - `400 Bad Request`: Invalid schema
    ```json
    {
      "error": "invalid_schema",
      "details": "Missing required field: text"
    }
    ```

### Retrieve Insights
- **GET** `/api/v1/insights`
- **Query Parameters:**
  - `start_time` (required): ISO8601 timestamp
  - `end_time` (required): ISO8601 timestamp
  - `limit` (optional): Max results (default: 100, max: 1000)
  - `min_confidence` (optional): Minimum confidence score (0.0-1.0)
  - `sentiment` (optional): Filter by sentiment (`positive`, `negative`, `neutral`)
- **Example:**
  ```bash
  curl "http://localhost:8000/api/v1/insights?start_time=2025-01-20T00:00:00Z&end_time=2025-01-21T00:00:00Z&limit=100"
  ```
- **Response:**
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

## Data Ingestion

### Using Sample Data
```bash
python ingest_data.py
```

### Using Kaggle Dataset
1. Download the Customer Support on Twitter dataset from [Kaggle](https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter)
2. Save as `twitter_support.csv` in the project directory
3. Run:
   ```bash
   DATASET_CSV=twitter_support.csv python ingest_data.py
   ```

## Architecture

### Components
- **main.py**: FastAPI application with API endpoints
- **models.py**: SQLAlchemy database models
- **schemas.py**: Pydantic request/response schemas
- **database.py**: Database connection and session management
- **grok_client.py**: Grok API client with rate limiting
- **rate_limiter.py**: Rate limiting implementation
- **batch_processor.py**: Background batch processing system
- **ingest_data.py**: Data ingestion script

### Database Schema
- **Conversations**: Stores raw conversation data
- **Insights**: Stores Grok analysis results

### Rate Limiting
- **Inbound**: 100 requests/second
- **Grok API**: 10 calls/second (enforced via semaphore)

### Resource Constraints
The application is optimized to run within:
- CPU: 2 cores
- Memory: 1GB RAM
- Storage: 10GB

## Docker Commands

- View logs: `docker logs insights-platform`
- Stop container: `docker stop insights-platform`
- Start container: `docker start insights-platform`
- Remove container: `docker rm insights-platform`
- Rebuild and restart:
  ```bash
  docker stop insights-platform
  docker rm insights-platform
  docker build -t insights-platform .
  docker run -d -p 8000:8000 -e GROK_KEY="your-key" --name insights-platform insights-platform
  ```

## Testing

### Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Submit a conversation
curl -X POST http://localhost:8000/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great product! Highly recommend!",
    "author": "test_user"
  }'

# Wait a few seconds for processing, then retrieve insights
curl "http://localhost:8000/api/v1/insights?start_time=2025-01-01T00:00:00Z&end_time=2025-12-31T23:59:59Z&limit=10"
```

## Troubleshooting

### Rate Limit Errors
- If you see 429 errors, wait for the `retry_after` seconds before retrying
- The system automatically limits Grok API calls to 10/second

### Database Issues
- The database file `insights.db` is created automatically
- To reset, delete `insights.db` and restart the application

### Grok API Errors
- Ensure `GROK_KEY` environment variable is set correctly
- Check API key validity on console.x.ai
- Review logs for detailed error messages

## Environment Variables

- `GROK_KEY`: Your Grok API key (required)
- `DATABASE_URL`: Database connection string (default: `sqlite+aiosqlite:///./insights.db`)
- `API_URL`: API base URL for data ingestion (default: `http://localhost:8000`)

## License

This project is part of the xAI assessment.
