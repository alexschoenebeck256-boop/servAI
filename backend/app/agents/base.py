from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.models import Agent, AgentType, AgentLog
from app.llm.provider import get_llm_provider
from app.rag.service import get_rag_service

class BaseAgent(ABC):
    def __init__(self, business_id: UUID, agent_id: UUID, db: Session):
        self.business_id = business_id
        self.agent_id = agent_id
        self.db = db
        self.llm = get_llm_provider()
        self.rag = get_rag_service(db)
        self._status = "IDLE"

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        self._status = value
        # Update status in DB
        agent = self.db.query(Agent).filter(Agent.id == self.agent_id).first()
        if agent:
            agent.status = value
            self.db.commit()

    async def log_action(self, action: str, details: Dict[str, Any], status: str = "SUCCESS"):
        """Log an agent action to the audit log."""
        log = AgentLog(
            business_id=self.business_id,
            agent_id=self.agent_id,
            action=action,
            details=details,
            status=status
        )
        self.db.add(log)
        self.db.commit()

    @abstractmethod
    async def run_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific task assigned to the agent."""
        pass

    @abstractmethod
    async def handle_message(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Handle a direct message from a user or another agent."""
        pass

    async def get_context(self, query: str) -> str:
        """Helper to fetch RAG context."""
        docs = await self.rag.search(str(self.business_id), query)
        return "\n".join([d["content"] for d in docs])

    async def ask_llm(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        """Helper to call LLM and log it."""
        try:
            response = await self.llm.generate(prompt, system_prompt=system_prompt)
            await self.log_action("LLM_CALL", {
                "prompt": prompt,
                "system_prompt": system_prompt,
                "response": response
            })
            return response
        except Exception as e:
            await self.log_action("LLM_CALL", {
                "prompt": prompt,
                "system_prompt": system_prompt,
                "error": str(e)
            }, status="FAILURE")
            raise e
