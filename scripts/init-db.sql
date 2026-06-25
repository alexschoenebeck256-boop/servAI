-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- Enums
CREATE TYPE user_role AS ENUM ('OWNER', 'MANAGER', 'TECH');
CREATE TYPE lead_status AS ENUM ('NEW', 'QUALIFYING', 'BOOKED', 'DEAD');
CREATE TYPE job_status AS ENUM ('SCHEDULED', 'IN_PROGRESS', 'COMPLETED', 'CANCELLED');
CREATE TYPE invoice_status AS ENUM ('DRAFT', 'SENT', 'PAID', 'VOID');
CREATE TYPE agent_type AS ENUM ('CEO', 'SALES', 'CS', 'OPS', 'MARKETING', 'REPUTATION', 'FINANCE');
CREATE TYPE agent_status AS ENUM ('IDLE', 'WORKING', 'SLEEPING');
CREATE TYPE conversation_channel AS ENUM ('SMS', 'CALL', 'CHAT');
CREATE TYPE sender_type AS ENUM ('CUSTOMER', 'AGENT', 'SYSTEM');
CREATE TYPE task_status AS ENUM ('PENDING', 'IN_PROGRESS', 'COMPLETED', 'FAILED');

-- Tables
CREATE TABLE IF NOT EXISTS businesses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    industry TEXT,
    timezone TEXT DEFAULT 'UTC',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    email TEXT NOT NULL UNIQUE,
    hashed_password TEXT NOT NULL,
    role user_role NOT NULL DEFAULT 'TECH',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    first_name TEXT,
    last_name TEXT,
    phone TEXT,
    email TEXT,
    address JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS leads (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE SET NULL,
    status lead_status DEFAULT 'NEW',
    source TEXT,
    summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
    assigned_tech_id UUID REFERENCES users(id) ON DELETE SET NULL,
    scheduled_at TIMESTAMPTZ,
    status job_status DEFAULT 'SCHEDULED',
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
    amount DECIMAL(12, 2),
    status invoice_status DEFAULT 'DRAFT',
    due_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS agents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    agent_type agent_type NOT NULL,
    status agent_status DEFAULT 'IDLE',
    config JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id) ON DELETE CASCADE,
    channel conversation_channel NOT NULL,
    status TEXT DEFAULT 'OPEN',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sender_type sender_type NOT NULL,
    sender_id UUID, -- Can be customer_id or agent_id
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    assigned_to_agent_id UUID REFERENCES agents(id) ON DELETE SET NULL,
    title TEXT NOT NULL,
    description TEXT,
    status task_status DEFAULT 'PENDING',
    result JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS knowledge_bases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS knowledge_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    kb_id UUID NOT NULL REFERENCES knowledge_bases(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_users_business_id ON users(business_id);
CREATE INDEX IF NOT EXISTS idx_customers_business_id ON customers(business_id);
CREATE INDEX IF NOT EXISTS idx_leads_business_id ON leads(business_id);
CREATE INDEX IF NOT EXISTS idx_jobs_business_id ON jobs(business_id);
CREATE INDEX IF NOT EXISTS idx_invoices_business_id ON invoices(business_id);
CREATE INDEX IF NOT EXISTS idx_agents_business_id ON agents(business_id);
CREATE INDEX IF NOT EXISTS idx_conversations_business_id ON conversations(business_id);
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX IF NOT EXISTS idx_tasks_business_id ON tasks(business_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_bases_business_id ON knowledge_bases(business_id);
CREATE INDEX IF NOT EXISTS idx_knowledge_documents_kb_id ON knowledge_documents(kb_id);

-- Row-Level Security (RLS) Policies
-- Enable RLS on all tables
ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE leads ENABLE ROW LEVEL SECURITY;
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE agents ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_bases ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_documents ENABLE ROW LEVEL SECURITY;

-- Note: In a real multi-tenant app, the app_user would be set via 
-- SET LOCAL app.current_business_id = 'uuid';
-- We define a helper function or just use the setting.

CREATE OR REPLACE FUNCTION get_current_business_id() RETURNS UUID AS $$
    SELECT current_setting('app.current_business_id', true)::UUID;
$$ LANGUAGE sql STABLE;

-- Business Policy: Only see your own business
CREATE POLICY business_isolation_policy ON businesses
    USING (id = get_current_business_id());

-- Generic tenant isolation policies
CREATE POLICY tenant_users_policy ON users USING (business_id = get_current_business_id());
CREATE POLICY tenant_customers_policy ON customers USING (business_id = get_current_business_id());
CREATE POLICY tenant_leads_policy ON leads USING (business_id = get_current_business_id());
CREATE POLICY tenant_jobs_policy ON jobs USING (business_id = get_current_business_id());
CREATE POLICY tenant_invoices_policy ON invoices USING (business_id = get_current_business_id());
CREATE POLICY tenant_agents_policy ON agents USING (business_id = get_current_business_id());
CREATE POLICY tenant_conversations_policy ON conversations USING (business_id = get_current_business_id());
CREATE POLICY tenant_tasks_policy ON tasks USING (business_id = get_current_business_id());
CREATE POLICY tenant_kb_policy ON knowledge_bases USING (business_id = get_current_business_id());

-- Messages and knowledge_documents are tied via parent tables
CREATE POLICY tenant_messages_policy ON messages
    USING (conversation_id IN (SELECT id FROM conversations WHERE business_id = get_current_business_id()));

CREATE POLICY tenant_knowledge_documents_policy ON knowledge_documents
    USING (kb_id IN (SELECT id FROM knowledge_bases WHERE business_id = get_current_business_id()));
