"""Database models for conversations and insights."""
from sqlalchemy import Column, String, Float, DateTime, JSON, Integer, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()


class Conversation(Base):
    """Stores raw conversation data from Twitter."""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: f"conv_{uuid.uuid4().hex[:8]}")
    text = Column(String, nullable=False)
    author = Column(String)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    raw_data = Column(JSON)  # Store original tweet data
    status = Column(String, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_conv_timestamp', 'timestamp'),
        Index('idx_conv_status', 'status'),
    )


class Insight(Base):
    """Stores Grok analysis results for conversations."""
    __tablename__ = "insights"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    text = Column(String, nullable=False)
    
    # Grok analysis results
    sentiment_score = Column(Float)  # -1.0 to 1.0
    clusters = Column(JSON)  # List of topic clusters
    confidence = Column(Float)  # 0.0 to 1.0
    reasoning = Column(String)
    
    # Full Grok response for debugging
    grok_analysis = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_insight_conversation_id', 'conversation_id'),
        Index('idx_insight_timestamp', 'timestamp'),
        Index('idx_insight_sentiment', 'sentiment_score'),
        Index('idx_insight_confidence', 'confidence'),
    )

