from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, Customer
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

router = APIRouter()

class CustomerSchema(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    phone: str
    address: Any
    created_at: datetime

    class Config:
        from_attributes = True

@router.get("/", response_model=List[CustomerSchema])
def read_customers(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    customers = db.query(Customer).filter(Customer.business_id == current_user.business_id).offset(skip).limit(limit).all()
    return customers
