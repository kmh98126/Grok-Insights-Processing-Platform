"""Background batch processor for analyzing conversations."""
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Conversation, Insight
from grok_client import analyze_conversation
from datetime import datetime
import logging
from database import AsyncSessionLocal

logger = logging.getLogger(__name__)

class BatchProcessor:
    """Processes conversations in batches using Grok API."""
    
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
        self.running = False
        self.task = None
    
    async def start(self):
        """Start the batch processor."""
        if self.running:
            return
        
        self.running = True
        self.task = asyncio.create_task(self._process_loop())
        logger.info("Batch processor started")
    
    async def stop(self):
        """Stop the batch processor."""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("Batch processor stopped")
    
    async def _process_loop(self):
        """Main processing loop."""
        while self.running:
            try:
                # Create a new session for each batch
                async with AsyncSessionLocal() as db:
                    # Get pending conversations
                    result = await db.execute(
                        select(Conversation)
                        .where(Conversation.status == "pending")
                        .limit(self.batch_size)
                    )
                    conversations = result.scalars().all()
                    
                    if not conversations:
                        # No pending conversations, wait a bit
                        await asyncio.sleep(5)
                        continue
                    
                    # Process batch
                    await self._process_batch(db, conversations)
                
                # Small delay between batches to respect rate limits
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in batch processor: {e}")
                await asyncio.sleep(5)
    
    async def _process_batch(self, db: AsyncSession, conversations: list):
        """Process a batch of conversations."""
        tasks = []
        for conv in conversations:
            # Update status to processing
            conv.status = "processing"
            tasks.append(self._process_single(db, conv))
        
        # Process in parallel (respecting Grok rate limits)
        await asyncio.gather(*tasks, return_exceptions=True)
        await db.commit()
    
    async def _process_single(self, db: AsyncSession, conversation: Conversation):
        """Process a single conversation."""
        try:
            # Analyze with Grok
            analysis = await analyze_conversation(conversation.text)
            
            # Create insight record
            insight = Insight(
                conversation_id=conversation.id,
                timestamp=conversation.timestamp,
                text=conversation.text,
                sentiment_score=analysis["sentiment_score"],
                clusters=analysis["clusters"],
                confidence=analysis["confidence"],
                reasoning=analysis["reasoning"],
                grok_analysis=analysis,
            )
            
            db.add(insight)
            
            # Update conversation status
            conversation.status = "completed"
            
            logger.info(f"Processed conversation {conversation.id}")
            
        except Exception as e:
            logger.error(f"Error processing conversation {conversation.id}: {e}")
            conversation.status = "failed"


# Global batch processor instance
batch_processor = BatchProcessor(batch_size=10)

