from typing import Optional, List, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from app.schemas.business import Business
# Add a simple Customer schema here or import it
class CustomerShort(BaseModel):
    id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None

class MessageBase(BaseModel):
    content: str
    metadata: Optional[dict] = None

class MessageCreate(MessageBase):
    conversation_id: UUID
    sender_type: str
    sender_id: Optional[UUID] = None

class Message(MessageBase):
    id: UUID
    conversation_id: UUID
    sender_type: str
    sender_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationBase(BaseModel):
    customer_id: UUID
    channel: str
    status: Optional[str] = "OPEN"

class ConversationCreate(ConversationBase):
    pass

class Conversation(ConversationBase):
    id: UUID
    business_id: UUID
    messages: List[Message] = []
    customer: Optional[CustomerShort] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
