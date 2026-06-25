from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User
from app.services.knowledge_service import get_knowledge_service

router = APIRouter()

@router.post("/upload")
async def upload_document(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    file: UploadFile = File(...),
) -> Any:
    """Upload a document for RAG ingestion."""
    content = await file.read()
    # Assume it's text for now
    text_content = content.decode("utf-8")
    
    knowledge_service = get_knowledge_service(db)
    result = await knowledge_service.upload_document(
        business_id=str(current_user.business_id),
        content=text_content,
        metadata={"filename": file.filename}
    )
    return result

@router.get("/search")
async def search_knowledge(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    query: str,
) -> Any:
    """Search the business knowledge base."""
    knowledge_service = get_knowledge_service(db)
    results = await knowledge_service.search_knowledge(
        business_id=str(current_user.business_id),
        query=query
    )
    return results
