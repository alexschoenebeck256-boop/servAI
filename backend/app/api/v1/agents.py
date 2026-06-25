from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.core.database import get_db
from app.models.models import User, Agent, Task as AgentTask
from app.schemas.agent import Agent as AgentSchema, AgentCreate, AgentUpdate, AgentCommand

router = APIRouter()

@router.get("/", response_model=List[AgentSchema])
def read_agents(
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    agents = db.query(Agent).filter(Agent.business_id == current_user.business_id).offset(skip).limit(limit).all()
    return agents

@router.get("/{id}", response_model=AgentSchema)
def read_agent(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    id: str,
) -> Any:
    agent = db.query(Agent).filter(Agent.id == id, Agent.business_id == current_user.business_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.post("/{id}/command")
def send_agent_command(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_active_user),
    id: str,
    command: AgentCommand,
) -> Any:
    agent = db.query(Agent).filter(Agent.id == id, Agent.business_id == current_user.business_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # In a real app, this would trigger an async task or push to a queue
    # For the scaffold, we'll just create a task record
    task = AgentTask(
        business_id=current_user.business_id,
        assigned_to_agent_id=agent.id,
        title=f"Command: {command.command}",
        description=str(command.params),
        status="PENDING"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    
    return {"status": "command_queued", "task_id": task.id}
