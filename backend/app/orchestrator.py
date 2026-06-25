from typing import Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.models import Agent, AgentType
from app.agents.registry import get_agent_instance
from app.core.database import SessionLocal

class AgentOrchestrator:
    def __init__(self):
        # Blackboard for shared state/events
        self.blackboard: Dict[str, Any] = {}

    async def trigger_event(self, event_name: str, payload: Dict[str, Any], business_id: UUID):
        """
        Handle events like 'new_lead', 'job_completed', etc.
        """
        db = SessionLocal()
        try:
            if event_name == "new_lead":
                await self._handle_new_lead(payload, business_id, db)
            elif event_name == "job_completed":
                await self._handle_job_completed(payload, business_id, db)
        finally:
            db.close()

    async def _handle_new_lead(self, payload: Dict[str, Any], business_id: UUID, db: Session):
        # Find the Sales Agent for this business
        agent_record = db.query(Agent).filter(
            Agent.business_id == business_id,
            Agent.agent_type == AgentType.SALES
        ).first()
        
        if agent_record:
            agent = get_agent_instance(AgentType.SALES, business_id, agent_record.id, db)
            # Assign task to Sales Agent
            await agent.run_task({
                "action": "qualify_lead",
                "lead_id": payload.get("lead_id")
            })

    async def _handle_job_completed(self, payload: Dict[str, Any], business_id: UUID, db: Session):
        # Find the CS Agent
        agent_record = db.query(Agent).filter(
            Agent.business_id == business_id,
            Agent.agent_type == AgentType.CS
        ).first()
        
        if agent_record:
            agent = get_agent_instance(AgentType.CS, business_id, agent_record.id, db)
            await agent.run_task({
                "action": "follow_up",
                "job_id": payload.get("job_id")
            })

orchestrator = AgentOrchestrator()
