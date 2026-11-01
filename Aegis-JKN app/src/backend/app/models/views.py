"""Database views for reporting and analytics."""
from sqlalchemy import (
    Column,
    String,
    Numeric,
    DateTime,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import DeclarativeBase

from src.backend.app.models.base import Base


class ProviderMonthlyOvercharge(Base):
    """
    Materialized view for aggregated overcharge per provider per month.

    This view aggregates claims data to show:
    - Total claimed amount per provider per month
    - Total expected/approved amount per provider per month
    - Overcharge amount (claimed - expected)
    - Claim count per provider per month
    - Average risk score per provider per month

    Refresh with: REFRESH MATERIALIZED VIEW provider_monthly_overcharge;
    """
    __tablename__ = "provider_monthly_overcharge"
    __table_args__ = {"info": dict(is_view=True)}

    # Primary key columns for the view
    provider_id = Column(PGUUID(as_uuid=True), primary_key=True)
    provider_name = Column(String)
    year_month = Column(String, primary_key=True)  # Format: YYYY-MM

    # Aggregated metrics
    total_claimed = Column(Numeric(precision=15, scale=2))
    total_expected = Column(Numeric(precision=15, scale=2))
    overcharge_amount = Column(Numeric(precision=15, scale=2))
    claim_count = Column(Numeric(precision=15, scale=0))
    avg_risk_score = Column(Numeric(precision=5, scale=4))

    # Timestamp of view refresh
    refreshed_at = Column(DateTime(timezone=True))


# SQL for creating the materialized view
PROVIDER_MONTHLY_OVERCHARGE_VIEW_SQL = """
CREATE MATERIALIZED VIEW IF NOT EXISTS provider_monthly_overcharge AS
SELECT
    p.id AS provider_id,
    p.name AS provider_name,
    to_char(c.created_at, 'YYYY-MM') AS year_month,
    SUM(c.amount) AS total_claimed,
    SUM(c.amount * (1 - COALESCE(c.risk_score, 0))) AS total_expected,
    SUM(c.amount * COALESCE(c.risk_score, 0)) AS overcharge_amount,
    COUNT(*) AS claim_count,
    AVG(c.risk_score) AS avg_risk_score,
    now() AS refreshed_at
FROM claims c
JOIN providers p ON c.provider_id = p.id
GROUP BY p.id, p.name, to_char(c.created_at, 'YYYY-MM')
WITH DATA;

-- Unique index for fast lookups
CREATE UNIQUE INDEX IF NOT EXISTS idx_provider_monthly_overcharge_pk
ON provider_monthly_overcharge (provider_id, year_month);

-- Index for time-range queries
CREATE INDEX IF NOT EXISTS idx_provider_monthly_overcharge_ym
ON provider_monthly_overcharge (year_month DESC);
"""

# Function to refresh the materialized view
REFRESH_PROVIDER_MONTHLY_OVERCHARGE_SQL = """
REFRESH MATERIALIZED VIEW CONCURRENTLY provider_monthly_overcharge;
"""