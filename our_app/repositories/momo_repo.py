# repositories/momo_repo.py
from typing import Sequence, Optional
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from our_app.core.postgres import MomoProfitRecord, get_db

class MomoRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    # ── CREATE ──
    async def create(self, record: MomoProfitRecord) -> MomoProfitRecord:
        self.db.add(record)
        await self.db.commit()
        await self.db.refresh(record)
        return record

    # ── READ ALL ──
    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
        momo_type: Optional[str] = None
    ) -> Sequence[MomoProfitRecord]:
        query = select(MomoProfitRecord).offset(skip).limit(limit).order_by(MomoProfitRecord.id.desc())
        if momo_type:
            query = query.where(MomoProfitRecord.momo_type == momo_type)
        result = await self.db.execute(query)
        return result.scalars().all()

    # ── READ ONE ──
    async def get_by_id(self, record_id: int) -> Optional[MomoProfitRecord]:
        query = select(MomoProfitRecord).where(MomoProfitRecord.id == record_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    # ── UPDATE ──
    async def update(self, record_id: int, updates: dict) -> Optional[MomoProfitRecord]:
        query = (
            update(MomoProfitRecord)
            .where(MomoProfitRecord.id == record_id)
            .values(**updates)
            .returning(MomoProfitRecord)
        )
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalar_one_or_none()

    # ── DELETE ──
    async def delete(self, record_id: int) -> bool:
        query = delete(MomoProfitRecord).where(MomoProfitRecord.id == record_id)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.rowcount > 0


# Dependency – inject this in routes
async def get_momo_repo(db: AsyncSession = Depends(get_db)) -> MomoRepository:
    return MomoRepository(db)