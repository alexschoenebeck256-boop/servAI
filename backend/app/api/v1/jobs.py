from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, Job
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

router = APIRouter()

class JobSchema(BaseModel):
    id: UUID
    status: str
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    created_at: datetime
    # Add other fields as needed

    class Config:
        from_attributes = True

@router.get("/", response_model=List[JobSchema])
def read_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    jobs = db.query(Job).filter(Job.business_id == current_user.business_id).offset(skip).limit(limit).all()
    return jobs
