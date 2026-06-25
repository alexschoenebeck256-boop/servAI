import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.models import Business, User, Agent
from app.core.security import get_password_hash

SQLALCHEMY_DATABASE_URI = "sqlite:///./servai.db"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed():
    db = SessionLocal()
    
    # Create Business
    business_id = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        business = Business(
            id=business_id,
            name="ServAI Demo Business",
            industry="HVAC"
        )
        db.add(business)
        db.commit()
        db.refresh(business)
    
    # Create User
    user = db.query(User).filter(User.email == "demo@servai.com").first()
    if not user:
        user = User(
            id=uuid.uuid4(),
            email="demo@servai.com",
            hashed_password="dummy_hash",
            full_name="Demo User",
            business_id=business.id,
            is_active=True,
            is_superuser=True
        )
        db.add(user)
        db.commit()
    
    # Create Agents
    agent_types = ["CEO", "MARKETING", "SALES", "CS", "OPS", "REPUTATION", "FINANCE"]
    for atype in agent_types:
        agent = db.query(Agent).filter(Agent.business_id == business.id, Agent.agent_type == atype).first()
        if not agent:
            agent = Agent(
                id=uuid.uuid4(),
                business_id=business.id,
                name=f"{atype.capitalize()} Agent",
                agent_type=atype,
                status="IDLE",
                config={}
            )
            db.add(agent)
    
    db.commit()
    db.close()
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
