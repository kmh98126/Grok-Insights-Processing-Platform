"""Grok API client for sentiment analysis and topic clustering."""
import os
import json
import httpx
from typing import Dict, Optional
import asyncio
from datetime import datetime

GROK_API_URL = "https://api.x.ai/v1/chat/completions"
GROK_API_KEY = os.getenv("GROK_KEY")

# Rate limiting: 10 calls/second to Grok
_grok_semaphore = asyncio.Semaphore(10)  # Allow 10 concurrent calls
_last_call_times = []
_call_interval = 0.1  # 100ms between calls = 10 calls/second


async def analyze_conversation(text: str) -> Dict:
    """
    Analyze conversation using Grok API for sentiment and clustering.
    
    Returns:
        {
            "sentiment_score": float (-1.0 to 1.0),
            "clusters": List[str],
            "confidence": float (0.0 to 1.0),
            "reasoning": str
        }
    """
    if not GROK_API_KEY:
        raise ValueError("GROK_KEY environment variable not set")
    
    # Rate limiting: ensure we don't exceed 10 calls/second
    async with _grok_semaphore:
        current_time = datetime.now().timestamp()
        
        # Remove calls older than 1 second
        global _last_call_times
        _last_call_times = [t for t in _last_call_times if current_time - t < 1.0]
        
        # If we have 10 calls in the last second, wait
        if len(_last_call_times) >= 10:
            wait_time = 1.0 - (current_time - _last_call_times[0])
            if wait_time > 0:
                await asyncio.sleep(wait_time)
        
        _last_call_times.append(datetime.now().timestamp())
        
        # Prepare prompt for Grok
        prompt = f"""Analyze the following Twitter conversation and provide insights in JSON format.

Conversation text: "{text}"

Please analyze and return a JSON object with the following structure:
{{
    "sentiment_score": <float between -1.0 (very negative) and 1.0 (very positive)>,
    "clusters": [<list of topic categories like "product_issues", "delivery_problems", "praise", "complaint", etc.>],
    "confidence": <float between 0.0 and 1.0 indicating confidence in the analysis>,
    "reasoning": "<brief explanation of the analysis>"
}}

Focus on:
1. Sentiment: Determine if the sentiment is positive, negative, or neutral
2. Topics: Identify main themes (e.g., "product_issues", "delivery_problems", "customer_support", "praise", "complaint")
3. Confidence: Assess how clear the sentiment and topics are

Return ONLY valid JSON, no additional text."""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROK_API_KEY}",
        }
        
        data = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "model": "grok-4-latest",
            "stream": False,
            "temperature": 0.3,  # Lower temperature for more consistent analysis
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = await client.post(GROK_API_URL, json=data, headers=headers)
                    response.raise_for_status()
                    
                    result = response.json()
                    content = result["choices"][0]["message"]["content"]
                    
                    # Parse JSON from Grok response
                    # Sometimes Grok wraps JSON in markdown code blocks
                    content = content.strip()
                    if content.startswith("```json"):
                        content = content[7:]
                    if content.startswith("```"):
                        content = content[3:]
                    if content.endswith("```"):
                        content = content[:-3]
                    content = content.strip()
                    
                    analysis = json.loads(content)
                    
                    # Validate and normalize response
                    return {
                        "sentiment_score": float(analysis.get("sentiment_score", 0.0)),
                        "clusters": analysis.get("clusters", []),
                        "confidence": float(analysis.get("confidence", 0.5)),
                        "reasoning": analysis.get("reasoning", "Analysis completed"),
                    }
                    
                except json.JSONDecodeError as e:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)  # Exponential backoff
                        continue
                    # Fallback response if JSON parsing fails
                    return {
                        "sentiment_score": 0.0,
                        "clusters": ["unknown"],
                        "confidence": 0.0,
                        "reasoning": f"Failed to parse Grok response: {str(e)}",
                    }
                    
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 429:  # Rate limit
                        retry_after = int(e.response.headers.get("Retry-After", 5))
                        await asyncio.sleep(retry_after)
                        continue
                    raise
                    
                except Exception as e:
                    if attempt < max_retries - 1:
                        await asyncio.sleep(2 ** attempt)
                        continue
                    raise

