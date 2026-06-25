from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, Invoice
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from decimal import Decimal

router = APIRouter()

class InvoiceSchema(BaseModel):
    id: UUID
    amount: Decimal
    status: str
    due_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[InvoiceSchema])
def read_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    invoices = db.query(Invoice).filter(Invoice.business_id == current_user.business_id).offset(skip).limit(limit).all()
    return invoices
