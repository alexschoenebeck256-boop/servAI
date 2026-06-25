import uuid
from sqlalchemy import Column, String, ForeignKey, Boolean, DateTime, DECIMAL, JSON, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base_model import Base, TimestampMixin
import enum

class UserRole(str, enum.Enum):
    OWNER = "OWNER"
    MANAGER = "MANAGER"
    TECH = "TECH"

class AgentType(str, enum.Enum):
    CEO = "CEO"
    SALES = "SALES"
    CS = "CS"
    OPS = "OPS"
    MARKETING = "MARKETING"
    REPUTATION = "REPUTATION"
    FINANCE = "FINANCE"

class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    QUALIFYING = "QUALIFYING"
    BOOKED = "BOOKED"
    DEAD = "DEAD"

class JobStatus(str, enum.Enum):
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class InvoiceStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    PAID = "PAID"
    VOID = "VOID"

class Business(Base, TimestampMixin):
    __tablename__ = "businesses"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    industry = Column(String)
    timezone = Column(String, default="UTC")
    
    users = relationship("User", back_populates="business")
    customers = relationship("Customer", back_populates="business")

class User(Base, TimestampMixin):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.TECH)
    is_active = Column(Boolean, default=True)

    business = relationship("Business", back_populates="users")

class Customer(Base, TimestampMixin):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    email = Column(String)
    address = Column(JSON)

    business = relationship("Business", back_populates="customers")
    conversations = relationship("Conversation", back_populates="customer")

class Lead(Base, TimestampMixin):
    __tablename__ = "leads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"))
    status = Column(Enum(LeadStatus), default=LeadStatus.NEW)
    source = Column(String)
    summary = Column(String)

    customer = relationship("Customer")

class Job(Base, TimestampMixin):
    __tablename__ = "jobs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    lead_id = Column(UUID(as_uuid=True), ForeignKey("leads.id"))
    assigned_tech_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    scheduled_at = Column(DateTime(timezone=True))
    status = Column(Enum(JobStatus), default=JobStatus.SCHEDULED)
    description = Column(String)

class Invoice(Base, TimestampMixin):
    __tablename__ = "invoices"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("jobs.id"))
    amount = Column(DECIMAL(10, 2))
    status = Column(Enum(InvoiceStatus), default=InvoiceStatus.DRAFT)
    due_at = Column(DateTime(timezone=True))

class Agent(Base, TimestampMixin):
    __tablename__ = "agents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    agent_type = Column(Enum(AgentType), nullable=False)
    status = Column(String) # IDLE, WORKING, SLEEPING
    config = Column(JSON)

class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    channel = Column(String) # SMS, CALL, CHAT
    status = Column(String) # OPEN, CLOSED

    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base, TimestampMixin):
    __tablename__ = "messages"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"), nullable=False)
    sender_type = Column(String) # CUSTOMER, AGENT, SYSTEM
    sender_id = Column(UUID(as_uuid=True)) # Can be user_id, agent_id, or customer_id
    content = Column(String)
    extra_metadata = Column(JSON)

    conversation = relationship("Conversation", back_populates="messages")

class Task(Base, TimestampMixin):
    __tablename__ = "agent_tasks" # 'tasks' might conflict with something
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    assigned_to_agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"))
    title = Column(String)
    description = Column(String)
    status = Column(String) # PENDING, IN_PROGRESS, COMPLETED, FAILED
    result = Column(JSON)

class AgentLog(Base, TimestampMixin):
    __tablename__ = "agent_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    business_id = Column(UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False)
    agent_id = Column(UUID(as_uuid=True), ForeignKey("agents.id"))
    action = Column(String) # e.g., "LLM_CALL", "TASK_EXECUTION"
    details = Column(JSON)
    status = Column(String) # "SUCCESS", "FAILURE"
