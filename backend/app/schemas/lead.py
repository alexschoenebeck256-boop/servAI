from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from app.models.models import LeadStatus

from app.schemas.conversation import CustomerShort

class LeadBase(BaseModel):
    customer_id: Optional[UUID] = None
    status: Optional[LeadStatus] = LeadStatus.NEW
    source: Optional[str] = None
    summary: Optional[str] = None

class LeadCreate(LeadBase):
    pass

class LeadUpdate(LeadBase):
    pass

class LeadInDBBase(LeadBase):
    id: UUID
    business_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Lead(LeadInDBBase):
    customer: Optional[CustomerShort] = None
