# Testing Guide

## Test Steps

### 1. Local Environment Testing

#### 1.1 Start Server
```bash
# Activate virtual environment
source venv/bin/activate

# Set environment variable
export GROK_KEY="your-api-key-here"

# Start server
uvicorn main:app --reload
```

#### 1.2 Health Check
```bash
curl http://localhost:8000/health
# Expected response: {"status":"ok"}
```

#### 1.3 Submit Conversation Test
```bash
curl -X POST http://localhost:8000/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Great product! Highly recommend!",
    "author": "test_user"
  }'
# Expected: {"status":"accepted","conversation_id":"conv_...","message":"Conversation queued for analysis"}
```

#### 1.4 Retrieve Insights Test
```bash
# Wait ~10 seconds for batch processing, then:
curl "http://localhost:8000/api/v1/insights?start_time=2025-01-01T00:00:00Z&end_time=2025-12-31T23:59:59Z&limit=10"
```

#### 1.5 Automated Test Script
```bash
./test_api.sh
```

### 2. Docker Testing

#### 2.1 Build Docker Image
```bash
docker build -t insights-platform .
```

#### 2.2 Run Docker Container
```bash
docker run -d -p 8000:8000 \
  -e GROK_KEY="your-api-key-here" \
  --name insights-platform \
  insights-platform
```

#### 2.3 Check Logs
```bash
docker logs insights-platform
```

#### 2.4 Run Tests
```bash
./test_api.sh
```

#### 2.5 Stop and Remove Container
```bash
docker stop insights-platform
docker rm insights-platform
```

### 3. Docker Compose Testing

#### 3.1 Set Environment Variable
```bash
export GROK_KEY="your-api-key-here"
```

#### 3.2 Start Services
```bash
docker-compose up -d
```

#### 3.3 Check Logs
```bash
docker-compose logs -f
```

#### 3.4 Run Tests
```bash
./test_api.sh
```

#### 3.5 Stop Services
```bash
docker-compose down
```

## Test Checklist

### Basic Functionality
- [ ] Health check response verification
- [ ] Conversation submission (202 Accepted)
- [ ] Rate limit test (429 response)
- [ ] Invalid request (400 Bad Request)
- [ ] Insights retrieval (with filtering)

### Grok Integration
- [ ] Batch processor processes conversations
- [ ] Sentiment score in range -1.0 to 1.0
- [ ] Clusters array returned
- [ ] Confidence score in range 0.0 to 1.0

### Rate Limiting
- [ ] 100 req/s limit working
- [ ] Retry-After header present
- [ ] Grok API 10 calls/s limit working

### Database
- [ ] Conversations saved
- [ ] Insights saved
- [ ] Query filtering working

## Troubleshooting

### Server Won't Start
- Check GROK_KEY environment variable
- Check if port 8000 is in use: `lsof -ti:8000`

### Batch Processor Not Working
- Check logs: `docker logs insights-platform`
- Verify pending conversations exist in database

### Grok API Errors
- Verify API key validity
- Check for rate limit exceeded
- Review detailed error messages in logs

## Performance Testing

### Bulk Data Ingestion
```bash
python ingest_data.py
```

### Concurrent Request Test
```bash
# 10 concurrent requests
for i in {1..10}; do
  curl -X POST http://localhost:8000/api/v1/conversations \
    -H "Content-Type: application/json" \
    -d "{\"text\": \"Test $i\"}" &
done
wait
```

## Example Test Scenarios

### Scenario 1: Positive Sentiment
```bash
curl -X POST http://localhost:8000/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{"text": "Amazing product! 5 stars!", "author": "happy_customer"}'
```
Expected: sentiment_score > 0.5, clusters include "praise"

### Scenario 2: Negative Sentiment
```bash
curl -X POST http://localhost:8000/api/v1/conversations \
  -H "Content-Type: application/json" \
  -d '{"text": "Terrible service. Very disappointed.", "author": "unhappy_customer"}'
```
Expected: sentiment_score < -0.5, clusters include "complaint"

### Scenario 3: Filtering
```bash
# Get only positive insights
curl "http://localhost:8000/api/v1/insights?start_time=2025-01-01T00:00:00Z&end_time=2025-12-31T23:59:59Z&sentiment=positive&limit=10"
```

