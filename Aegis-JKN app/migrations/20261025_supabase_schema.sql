-- ============================================================================
-- Aegis-JKN Supabase / PostgreSQL Self-Hosted Migration Schema
-- Target: Supabase Postgres v15+ (Self-Hosted / Cloud)
-- Tables: claims, audit_logs, graph_nodes
-- ============================================================================

-- 1. EXTENSIONS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 2. TABEL CLAIMS (Berkas Klaim & Keputusan Verifikasi)
CREATE TABLE IF NOT EXISTS public.claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id VARCHAR(100) UNIQUE NOT NULL,
    patient_id VARCHAR(100),
    provider_id VARCHAR(100),
    patient_name VARCHAR(255),
    hospital_name VARCHAR(255),
    doctor_name VARCHAR(255),
    diagnosis_icd10 VARCHAR(50),
    procedure_icd9 VARCHAR(50),
    service_type VARCHAR(50),
    amount DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    risk_score FLOAT DEFAULT 0.0,
    risk_level VARCHAR(50),             -- 'fraud' | 'high' | 'medium' | 'low'
    modus VARCHAR(255),
    syndicate VARCHAR(100),
    verified_status VARCHAR(50),        -- 'APPROVE' | 'CLARIFY_RS' | 'ESCALATE_P2PK'
    verifier_note TEXT,
    verified_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_claims_claim_id ON public.claims(claim_id);
CREATE INDEX IF NOT EXISTS idx_claims_verified_status ON public.claims(verified_status);
CREATE INDEX IF NOT EXISTS idx_claims_risk_level ON public.claims(risk_level);
CREATE INDEX IF NOT EXISTS idx_claims_hospital ON public.claims(hospital_name);

-- 3. TABEL AUDIT LOGS (Append-Only Cryptographic Log Chain)
CREATE TABLE IF NOT EXISTS public.audit_logs (
    id VARCHAR(100) PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    claim_id VARCHAR(100),
    action VARCHAR(100) NOT NULL,
    verifier_id VARCHAR(100),
    note TEXT,
    ai_score FLOAT,
    modus VARCHAR(255),
    syndicate VARCHAR(100),
    sha256_hash VARCHAR(64) NOT NULL,
    prev_hash VARCHAR(64),
    signature TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_audit_logs_claim_id ON public.audit_logs(claim_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_timestamp ON public.audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_logs_hash ON public.audit_logs(sha256_hash);

-- 4. TABEL GRAPH NODES (Graphiti Bi-temporal / MiroFish Topology)
CREATE TABLE IF NOT EXISTS public.graph_nodes (
    id VARCHAR(100) PRIMARY KEY,
    label VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,          -- 'patient' | 'doctor' | 'hospital' | 'diagnosis' | 'procedure'
    risk VARCHAR(50),                   -- 'fraud' | 'high' | 'medium' | 'low'
    detail TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    valid_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    invalid_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_graph_nodes_type ON public.graph_nodes(type);
CREATE INDEX IF NOT EXISTS idx_graph_nodes_risk ON public.graph_nodes(risk);
CREATE INDEX IF NOT EXISTS idx_graph_nodes_metadata ON public.graph_nodes USING GIN(metadata);

-- 5. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE public.claims ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.graph_nodes ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow read/write for authenticated users" ON public.claims
    FOR ALL USING (auth.role() = 'authenticated' OR auth.role() = 'anon');

CREATE POLICY "Allow read/write for authenticated users" ON public.audit_logs
    FOR ALL USING (auth.role() = 'authenticated' OR auth.role() = 'anon');

CREATE POLICY "Allow read/write for authenticated users" ON public.graph_nodes
    FOR ALL USING (auth.role() = 'authenticated' OR auth.role() = 'anon');
