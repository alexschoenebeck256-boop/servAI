from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, Lead
from app.schemas.lead import Lead as LeadSchema, LeadCreate, LeadUpdate

router = APIRouter()

@router.get("/", response_model=List[LeadSchema])
def read_leads(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    leads = db.query(Lead).filter(Lead.business_id == current_user.business_id).offset(skip).limit(limit).all()
    return leads

from app.queue.tasks import run_async_event

@router.post("/", response_model=LeadSchema)
def create_lead(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    lead_in: LeadCreate,
) -> Any:
    lead = Lead(**lead_in.dict(), business_id=current_user.business_id)
    db.add(lead)
    db.commit()
    db.refresh(lead)
    
    # Trigger AI qualification event
    run_async_event("new_lead", {"lead_id": str(lead.id)}, current_user.business_id)
    
    return lead

@router.get("/{id}", response_model=LeadSchema)
def read_lead(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    id: str,
) -> Any:
    lead = db.query(Lead).filter(Lead.id == id, Lead.business_id == current_user.business_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.patch("/{id}", response_model=LeadSchema)
def update_lead(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    id: str,
    lead_in: LeadUpdate,
) -> Any:
    lead = db.query(Lead).filter(Lead.id == id, Lead.business_id == current_user.business_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    update_data = lead_in.dict(exclude_unset=True)
    for field in update_data:
        setattr(lead, field, update_data[field])
    
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead
