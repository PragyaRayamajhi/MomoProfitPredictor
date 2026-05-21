"""
MongoDB repository for momo prediction logs.

Stores every prediction as a document so we have a fast,
schema-flexible event log alongside the Postgres source of truth.
"""
from datetime import datetime
from typing import Sequence
from fastapi import Depends
from pymongo.asynchronous.database import AsyncDatabase
from our_app.core.mongodb_async import get_async_mongo_database

COLLECTION = "momo_predictions"


def get_mongo_db() -> AsyncDatabase:
    return get_async_mongo_database()


class MomoMongoRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db[COLLECTION]

    async def log_prediction(
        self,
        momo_type: str,
        temperature: float,
        is_weekend: bool,
        is_festival: bool,
        predicted_profit: float,
        recommendation: str,
        confidence: str,
    ) -> str:
        doc = {
            "momo_type": momo_type,
            "temperature": temperature,
            "is_weekend": is_weekend,
            "is_festival": is_festival,
            "predicted_profit": predicted_profit,
            "recommendation": recommendation,
            "confidence": confidence,
            "created_at": datetime.utcnow(),
        }
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)

    async def recent(self, limit: int = 20) -> Sequence[dict]:
        cursor = self.collection.find().sort("created_at", -1).limit(limit)
        docs = []
        async for d in cursor:
            d["_id"] = str(d["_id"])
            docs.append(d)
        return docs

    async def count(self) -> int:
        return await self.collection.count_documents({})


async def get_momo_mongo_repo(
    db: AsyncDatabase = Depends(get_mongo_db),
) -> MomoMongoRepository:
    return MomoMongoRepository(db)
