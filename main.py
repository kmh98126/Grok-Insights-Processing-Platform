"""FastAPI application for Insights Platform."""
from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime
from typing import Optional
import logging

from database import get_db, init_db
from models import Conversation, Insight
from schemas import (
    ConversationRequest,
    ConversationResponse,
    InsightsResponse,
    InsightItem,
    GrokAnalysis,
    ErrorResponse,
    SentimentFilter,
)
from rate_limiter import inbound_limiter
from batch_processor import batch_processor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Insights Platform API",
    description="Backend API for analyzing Twitter conversations using Grok",
    version="1.0.0",
)


@app.on_event("startup")
async def startup_event():
    """Initialize database and start batch processor."""
    await init_db()
    logger.info("Database initialized")
    
    # Start batch processor in background
    await batch_processor.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Stop batch processor on shutdown."""
    await batch_processor.stop()
    logger.info("Application shutting down")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post(
    "/api/v1/conversations",
    response_model=ConversationResponse,
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        202: {"model": ConversationResponse},
        400: {"model": ErrorResponse},
        429: {"model": ErrorResponse},
    },
)
async def submit_conversation(
    request: ConversationRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Submit a new conversation for analysis.
    
    Returns 202 Accepted if queued successfully.
    Returns 429 if rate limit exceeded.
    Returns 400 if request is invalid.
    """
    # Rate limiting: 100 requests/second
    if not await inbound_limiter.acquire():
        retry_after = await inbound_limiter.get_retry_after()
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": "rate_limit_exceeded",
                "retry_after": retry_after,
            },
        )
    
    try:
        # Create conversation record
        conversation = Conversation(
            text=request.text,
            author=request.author,
            timestamp=request.timestamp or datetime.utcnow(),
            raw_data=request.raw_data,
            status="pending",
        )
        
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)
        
        logger.info(f"Queued conversation {conversation.id} for analysis")
        
        return ConversationResponse(
            status="accepted",
            conversation_id=conversation.id,
            message="Conversation queued for analysis",
        )
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error submitting conversation: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_schema",
                "details": str(e),
            },
        )


@app.get(
    "/api/v1/insights",
    response_model=InsightsResponse,
    responses={
        200: {"model": InsightsResponse},
        400: {"model": ErrorResponse},
    },
)
async def get_insights(
    start_time: datetime = Query(..., description="Start time (ISO8601)"),
    end_time: datetime = Query(..., description="End time (ISO8601)"),
    limit: int = Query(100, ge=1, le=1000, description="Max results"),
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum confidence score"),
    sentiment: Optional[SentimentFilter] = Query(None, description="Filter by sentiment"),
    db: AsyncSession = Depends(get_db),
):
    """
    Retrieve analysis results for conversations.
    
    Query parameters:
    - start_time: ISO8601 timestamp (required)
    - end_time: ISO8601 timestamp (required)
    - limit: max results (default: 100, max: 1000)
    - min_confidence: minimum Grok confidence score (optional, 0.0-1.0)
    - sentiment: filter by sentiment (positive/negative/neutral) (optional)
    """
    try:
        # Build query
        query = select(Insight).where(
            and_(
                Insight.timestamp >= start_time,
                Insight.timestamp <= end_time,
            )
        )
        
        # Apply filters
        if min_confidence is not None:
            query = query.where(Insight.confidence >= min_confidence)
        
        if sentiment:
            if sentiment == SentimentFilter.positive:
                query = query.where(Insight.sentiment_score > 0.1)
            elif sentiment == SentimentFilter.negative:
                query = query.where(Insight.sentiment_score < -0.1)
            elif sentiment == SentimentFilter.neutral:
                query = query.where(
                    and_(
                        Insight.sentiment_score >= -0.1,
                        Insight.sentiment_score <= 0.1,
                    )
                )
        
        # Order by timestamp descending
        query = query.order_by(Insight.timestamp.desc()).limit(limit)
        
        # Execute query
        result = await db.execute(query)
        insights = result.scalars().all()
        
        # Convert to response format
        insight_items = [
            InsightItem(
                conversation_id=insight.conversation_id,
                timestamp=insight.timestamp,
                text=insight.text,
                grok_analysis=GrokAnalysis(
                    sentiment_score=insight.sentiment_score,
                    clusters=insight.clusters or [],
                    confidence=insight.confidence,
                    reasoning=insight.reasoning,
                ),
            )
            for insight in insights
        ]
        
        # Get total count (for metadata)
        count_query = select(Insight).where(
            and_(
                Insight.timestamp >= start_time,
                Insight.timestamp <= end_time,
            )
        )
        if min_confidence is not None:
            count_query = count_query.where(Insight.confidence >= min_confidence)
        if sentiment:
            if sentiment == SentimentFilter.positive:
                count_query = count_query.where(Insight.sentiment_score > 0.1)
            elif sentiment == SentimentFilter.negative:
                count_query = count_query.where(Insight.sentiment_score < -0.1)
            elif sentiment == SentimentFilter.neutral:
                count_query = count_query.where(
                    and_(
                        Insight.sentiment_score >= -0.1,
                        Insight.sentiment_score <= 0.1,
                    )
                )
        
        count_result = await db.execute(count_query)
        total_count = len(count_result.scalars().all())
        
        return InsightsResponse(
            insights=insight_items,
            metadata={
                "total_count": total_count,
                "returned_count": len(insight_items),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
            },
        )
        
    except Exception as e:
        logger.error(f"Error retrieving insights: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": "invalid_query",
                "details": str(e),
            },
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
