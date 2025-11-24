"""Pydantic schemas for API requests and responses."""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class SentimentFilter(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"


class ConversationRequest(BaseModel):
    """Request schema for submitting a conversation."""
    text: str = Field(..., min_length=1, description="Conversation text content")
    author: Optional[str] = Field(None, description="Author/username")
    timestamp: Optional[datetime] = Field(None, description="Conversation timestamp")
    raw_data: Optional[dict] = Field(None, description="Additional metadata")
    
    @validator('text')
    def text_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('text cannot be empty')
        return v.strip()


class ConversationResponse(BaseModel):
    """Response schema for conversation submission."""
    status: str
    conversation_id: str
    message: str


class GrokAnalysis(BaseModel):
    """Grok analysis result schema."""
    sentiment_score: float = Field(..., ge=-1.0, le=1.0)
    clusters: List[str]
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: Optional[str] = None


class InsightItem(BaseModel):
    """Individual insight item in response."""
    conversation_id: str
    timestamp: datetime
    text: str
    grok_analysis: GrokAnalysis
    
    class Config:
        from_attributes = True


class InsightsResponse(BaseModel):
    """Response schema for insights retrieval."""
    insights: List[InsightItem]
    metadata: dict


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    details: Optional[str] = None
    retry_after: Optional[int] = None

