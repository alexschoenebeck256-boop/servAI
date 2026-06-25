from typing import Optional, List, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.models import AgentType

class AgentBase(BaseModel):
    agent_type: AgentType
    status: Optional[str] = "IDLE"
    config: Optional[dict] = None

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    pass

class AgentInDBBase(AgentBase):
    id: UUID
    business_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Agent(AgentInDBBase):
    pass

class AgentCommand(BaseModel):
    command: str
    params: Optional[dict] = None
