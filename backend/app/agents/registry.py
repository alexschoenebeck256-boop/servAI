from typing import Dict, Type, Any
from uuid import UUID
from sqlalchemy.orm import Session
from app.models.models import AgentType
from app.agents.base import BaseAgent
from app.agents.ceo import CEOAgent
from app.agents.sales import SalesAgent
from app.agents.cs import CSAgent
from app.agents.marketing import MarketingAgent
from app.agents.reputation import ReputationAgent
from app.agents.finance import FinanceAgent
from app.agents.ops import OpsAgent

AGENT_CLASSES: Dict[AgentType, Type[BaseAgent]] = {
    AgentType.CEO: CEOAgent,
    AgentType.SALES: SalesAgent,
    AgentType.CS: CSAgent,
    AgentType.MARKETING: MarketingAgent,
    AgentType.REPUTATION: ReputationAgent,
    AgentType.FINANCE: FinanceAgent,
    AgentType.OPS: OpsAgent,
}

def get_agent_instance(agent_type: AgentType, business_id: UUID, agent_id: UUID, db: Session) -> BaseAgent:
    agent_class = AGENT_CLASSES.get(agent_type)
    if not agent_class:
        raise ValueError(f"Agent type {agent_type} not implemented in registry.")
    return agent_class(business_id=business_id, agent_id=agent_id, db=db)
