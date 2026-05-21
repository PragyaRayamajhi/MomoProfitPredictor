"""
PostgreSQL database layer using SQLAlchemy.

Handles:
- Engine creation
- Declarative base
- Session factory
- Momo profit table
- Dependency injection
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from our_app.core.config import settings

engine = create_async_engine(settings.postgresql_url, echo=False)
# class_ = Async
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

"""
    SQLAlchemy model for momo profit predictions.

    Columns:
        id (int): Primary key
        momo_type (str): BUFF/CHICKEN/VEG
        temperature (float): Weather in °C
        is_weekend (str): "true"/"false"
        is_festival (str): "true"/"false"
        predicted_profit (float): Profit in NPR
        recommendation (str): AI suggestion
        confidence (str): High/Medium/Low
        created_at (datetime): Timestamp
    """
class MomoProfitRecord(Base):

    __tablename__ = "momo_profits"

    id = Column(Integer, primary_key=True, index=True)
    momo_type = Column(String, index=True)
    temperature = Column(Float)
    is_weekend = Column(Boolean)
    is_festival = Column(Boolean)
    predicted_profit = Column(Float)
    recommendation = Column(String)
    confidence = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables on startup (in lifespan)
async def get_db():
    """
    Dependency function to provide database session.

    Yields:
        Session: SQLAlchemy session object
    """
    async with AsyncSessionLocal() as session:
        yield session