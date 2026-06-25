from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, Conversation, Message
from app.schemas.conversation import Conversation as ConversationSchema, ConversationCreate, MessageCreate

router = APIRouter()

@router.get("/", response_model=List[ConversationSchema])
def read_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    conversations = db.query(Conversation).filter(Conversation.business_id == current_user.business_id).offset(skip).limit(limit).all()
    return conversations

@router.get("/{id}", response_model=ConversationSchema)
def read_conversation(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    id: str,
) -> Any:
    conversation = db.query(Conversation).filter(Conversation.id == id, Conversation.business_id == current_user.business_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.post("/{id}/messages", response_model=Any)
def send_message(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    id: str,
    message_in: MessageCreate,
) -> Any:
    conversation = db.query(Conversation).filter(Conversation.id == id, Conversation.business_id == current_user.business_id).first()
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    message = Message(
        conversation_id=conversation.id,
        sender_type=message_in.sender_type,
        sender_id=message_in.sender_id or current_user.id,
        content=message_in.content,
        metadata=message_in.metadata
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message
