"""Script to ingest sample data from Kaggle dataset or generate test data."""
import asyncio
import csv
import json
from datetime import datetime, timedelta
from pathlib import Path
import httpx
import os

# Sample test data if Kaggle dataset is not available
SAMPLE_CONVERSATIONS = [
    {
        "text": "Still waiting on my order... it's been 2 weeks. Very disappointed with the service.",
        "author": "customer123",
    },
    {
        "text": "Great product! Fast shipping and excellent quality. Highly recommend!",
        "author": "happy_customer",
    },
    {
        "text": "Having issues with my account. Can someone help?",
        "author": "user456",
    },
    {
        "text": "The delivery was delayed but customer service was very helpful. Thanks!",
        "author": "satisfied_user",
    },
    {
        "text": "Product arrived damaged. Need a refund immediately.",
        "author": "angry_customer",
    },
    {
        "text": "Love the new features! Keep up the great work!",
        "author": "fan_user",
    },
    {
        "text": "Billing issue - charged twice for the same order.",
        "author": "concerned_user",
    },
    {
        "text": "Best customer service experience ever! Thank you!",
        "author": "grateful_customer",
    },
    {
        "text": "Website is down. Can't access my account.",
        "author": "frustrated_user",
    },
    {
        "text": "Amazing product quality and fast response time. 5 stars!",
        "author": "reviewer_123",
    },
]


async def ingest_from_api(api_url: str, conversations: list):
    """Ingest conversations via API."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = []
        for conv in conversations:
            payload = {
                "text": conv["text"],
                "author": conv.get("author"),
                "timestamp": (datetime.utcnow() - timedelta(days=1)).isoformat(),
            }
            tasks.append(
                client.post(
                    f"{api_url}/api/v1/conversations",
                    json=payload,
                )
            )
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        success_count = sum(1 for r in results if isinstance(r, httpx.Response) and r.status_code == 202)
        print(f"Successfully ingested {success_count}/{len(conversations)} conversations")
        
        return success_count


async def ingest_from_csv(csv_path: str, api_url: str):
    """Ingest conversations from CSV file (Kaggle dataset format)."""
    conversations = []
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Adapt based on actual CSV columns
                text = row.get('text', row.get('tweet_text', ''))
                if text:
                    conversations.append({
                        "text": text,
                        "author": row.get('author_id', row.get('user_id', '')),
                    })
    except FileNotFoundError:
        print(f"CSV file not found: {csv_path}")
        return 0
    
    if conversations:
        return await ingest_from_api(api_url, conversations[:1000])  # Limit to 1000
    return 0


async def main():
    """Main ingestion function."""
    api_url = os.getenv("API_URL", "http://localhost:8000")
    
    print(f"Ingesting data to {api_url}")
    print("=" * 50)
    
    # Try to load from CSV if available
    csv_path = os.getenv("DATASET_CSV", "twitter_support.csv")
    if Path(csv_path).exists():
        print(f"Loading from CSV: {csv_path}")
        count = await ingest_from_csv(csv_path, api_url)
        if count > 0:
            print(f"✅ Ingested {count} conversations from CSV")
            return
    
    # Otherwise use sample data
    print("Using sample test data...")
    count = await ingest_from_api(api_url, SAMPLE_CONVERSATIONS)
    print(f"✅ Ingested {count} sample conversations")
    
    print("\n💡 To use Kaggle dataset:")
    print("   1. Download from: https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter")
    print("   2. Save as 'twitter_support.csv' in this directory")
    print("   3. Run: DATASET_CSV=twitter_support.csv python ingest_data.py")


if __name__ == "__main__":
    asyncio.run(main())

