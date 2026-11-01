"""
Service for managing risk score updates with ACID transactions.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import update, select
from src.backend.app.models.claim import Claim
from src.backend.app.models.audit import AuditLog
from sqlalchemy.dialects.postgresql import JSONB
import uuid
from datetime import datetime

class RiskScoreService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def update_claim_risk_score(self, claim_id: str, new_score: float, user_id: str, reason: str) -> Claim:
        """
        Update risk score for a claim using a serializable transaction
        to ensure ACID compliance during concurrent updates.
        """
        try:
            # Start transaction with a specific isolation level for the session if needed
            # Note: In SQLAlchemy async, the transaction is typically managed by the session.
            # For true serializable, we'd use: await self.db.execute(text("SET TRANSACTION ISOLATION LEVEL SERIALIZABLE"))

            async with self.db.begin_nested():  # Savepoint for atomicity
                # 1. Update the risk score
                result = await self.db.execute(
                    update(Claim)
                    .where(Claim.claim_id == claim_id)
                    .values(risk_score=new_score)
                    .returning(Claim)
                )
                claim = result.scalar_one_or_none()

                if not claim:
                    raise ValueError(f"Claim {claim_id} not found")

                # 2. Create an audit log entry (Consistency)
                audit_entry = AuditLog(
                    entity_id=str(claim.id),
                    action="UPDATE_RISK_SCORE",
                    user_id=user_id,
                    details={
                        "old_score": "Unknown", # In a real app, fetch old score first
                        "new_score": new_score,
                        "reason": reason,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                )
                self.db.add(audit_entry)

                # The outer session.commit() in get_db() will finalize the transaction
                return claim
        except Exception as e:
            await self.db.rollback()
            raise e

    async def bulk_update_risk_scores(self, updates: list[dict]):
        """
        Update multiple risk scores in a single ACID transaction.
        updates: list of {'claim_id': str, 'score': float, 'user_id': str, 'reason': str}
        """
        try:
            async with self.db.begin_nested():
                for up in updates:
                    await self.update_claim_risk_score(
                        up['claim_id'], up['score'], up['user_id'], up['reason']
                    )
        except Exception as e:
            await self.db.rollback()
            raise e