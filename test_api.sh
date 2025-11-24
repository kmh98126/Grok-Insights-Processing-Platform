#!/bin/bash

# API Test Script
API_URL="http://localhost:8000"

echo "🧪 Testing Insights Platform API"
echo "=================================="
echo ""

# 1. Health Check
echo "1️⃣ Testing Health Check..."
response=$(curl -s -w "\n%{http_code}" "$API_URL/health")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" == "200" ]; then
    echo "✅ Health check passed: $body"
else
    echo "❌ Health check failed: HTTP $http_code"
    exit 1
fi
echo ""

# 2. Submit Conversation
echo "2️⃣ Testing Conversation Submission..."
response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/conversations" \
    -H "Content-Type: application/json" \
    -d '{
        "text": "Great product! Fast shipping and excellent quality. Highly recommend!",
        "author": "test_user"
    }')
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" == "202" ]; then
    echo "✅ Conversation submitted: $body"
    CONV_ID=$(echo "$body" | grep -o '"conversation_id":"[^"]*"' | cut -d'"' -f4)
    echo "   Conversation ID: $CONV_ID"
else
    echo "❌ Submission failed: HTTP $http_code"
    echo "   Response: $body"
fi
echo ""

# 3. Submit Multiple Conversations
echo "3️⃣ Testing Multiple Submissions..."
for i in {1..3}; do
    response=$(curl -s -w "\n%{http_code}" -X POST "$API_URL/api/v1/conversations" \
        -H "Content-Type: application/json" \
        -d "{
            \"text\": \"Test conversation $i - This is a sample message for testing.\",
            \"author\": \"test_user_$i\"
        }")
    http_code=$(echo "$response" | tail -n1)
    if [ "$http_code" == "202" ]; then
        echo "   ✅ Conversation $i submitted"
    else
        echo "   ❌ Conversation $i failed: HTTP $http_code"
    fi
    sleep 0.1  # Small delay to avoid rate limiting
done
echo ""

# 4. Wait for Processing
echo "4️⃣ Waiting for batch processing (10 seconds)..."
sleep 10
echo ""

# 5. Get Insights
echo "5️⃣ Testing Insights Retrieval..."
START_TIME=$(date -u -v-1d +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%SZ")
END_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

response=$(curl -s -w "\n%{http_code}" "$API_URL/api/v1/insights?start_time=$START_TIME&end_time=$END_TIME&limit=10")
http_code=$(echo "$response" | tail -n1)
body=$(echo "$response" | head -n-1)

if [ "$http_code" == "200" ]; then
    echo "✅ Insights retrieved:"
    echo "$body" | python3 -m json.tool 2>/dev/null || echo "$body"
else
    echo "❌ Retrieval failed: HTTP $http_code"
    echo "   Response: $body"
fi
echo ""

echo "=================================="
echo "✅ Test completed!"
