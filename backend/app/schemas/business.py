from typing import Optional, Dict, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BusinessBase(BaseModel):
    name: str
    industry: Optional[str] = None
    timezone: Optional[str] = "UTC"

class BusinessCreate(BusinessBase):
    pass

class BusinessUpdate(BusinessBase):
    name: Optional[str] = None
    config: Optional[Dict[str, Any]] = None # For storing encrypted API keys etc

class BusinessInDBBase(BusinessBase):
    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Business(BusinessInDBBase):
    pass
