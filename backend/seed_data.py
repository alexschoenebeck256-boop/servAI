import uuid
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add the parent directory to sys.path to import from app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

from app.models.models import Business, User, Agent, AgentType
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URI = "sqlite:///./servai.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():
    db = SessionLocal()
    
    # Create Business
    business_id = uuid.uuid4()
    business = Business(
        id=business_id,
        name="ServAI Demo Business",
        industry="HVAC"
    )
    db.add(business)
    db.commit()
    db.refresh(business)
    print(f"Created Business: {business.id}")
    
    # Create User
    user = User(
        id=uuid.uuid4(),
        email="demo@servai.com",
        hashed_password="dummy_password_hash",
        business_id=business.id,
        is_active=True
    )
    db.add(user)
    db.commit()
    print(f"Created User: {user.email}")
    
    # Create Agents
    agent_types = [AgentType.CEO, AgentType.MARKETING, AgentType.SALES, AgentType.CS, AgentType.OPS, AgentType.REPUTATION, AgentType.FINANCE]
    for atype in agent_types:
        agent = Agent(
            id=uuid.uuid4(),
            business_id=business.id,
            agent_type=atype,
            status="IDLE",
            config={}
        )
        db.add(agent)
    
    db.commit()
    print("Created 7 AI Agents.")
    db.close()
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
