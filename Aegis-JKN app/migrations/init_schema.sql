-- Aegis-JKN Schema Initialization Script
-- Target: PostgreSQL Aurora

-- 1. Tables
CREATE TABLE IF NOT EXISTS user_roles (
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    permissions JSONB
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role_id INTEGER REFERENCES user_roles(id)
);

CREATE TABLE IF NOT EXISTS patients (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    patient_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    dob DATE,
    gender VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100),
    address TEXT
);

CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_id VARCHAR(100) UNIQUE NOT NULL,
    patient_id UUID NOT NULL REFERENCES patients(id),
    provider_id UUID NOT NULL REFERENCES providers(id),
    amount DECIMAL(15, 2) NOT NULL,
    status VARCHAR(50),
    risk_score FLOAT DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,
    entity_id VARCHAR(100),
    action VARCHAR(100) NOT NULL,
    user_id VARCHAR(100),
    details JSONB NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Indices
CREATE INDEX idx_claims_claim_id ON claims (claim_id);
CREATE INDEX idx_patients_patient_id ON patients (patient_id);
CREATE INDEX idx_providers_provider_id ON providers (provider_id);
CREATE INDEX idx_audit_details ON audit_logs USING GIN (details);

-- 3. Reporting View
-- Aggregated overcharge per Provider per month (High Risk > 0.8)
CREATE OR REPLACE VIEW view_provider_monthly_overcharge AS
SELECT
    p.name AS provider_name,
    DATE_TRUNC('month', c.created_at) AS report_month,
    SUM(c.amount) FILTER (WHERE c.risk_score > 0.8) AS total_high_risk_amount,
    COUNT(c.id) FILTER (WHERE c.risk_score > 0.8) AS high_risk_claim_count
FROM providers p
JOIN claims c ON p.id = c.provider_id
GROUP BY p.name, report_month;
