import asyncio
from typing import Dict, Any
from uuid import UUID
from app.orchestrator import orchestrator

async def process_agent_event(event_name: str, payload: Dict[str, Any], business_id: UUID):
    """
    Background task to process events asynchronously.
    """
    # In a real app, this would be a Celery task
    print(f"Background task: Processing event {event_name} for business {business_id}")
    await orchestrator.trigger_event(event_name, payload, business_id)

def run_async_event(event_name: str, payload: Dict[str, Any], business_id: UUID):
    """
    Fire and forget event processing.
    """
    asyncio.create_task(process_agent_event(event_name, payload, business_id))
