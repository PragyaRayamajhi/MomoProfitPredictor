"""
Configuration module for Momo Profit Predictor.

This module handles environment variables, database URLs,
and settings using Pydantic v2+ best practices.

"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Annotated
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from .env file.

    Attributes:
        PROJECT_NAME (str): Name of the application
        DEBUG (bool): Debug mode toggle
        POSTGRES_* (str): PostgreSQL connection details
        MONGO_URI (str): MongoDB connection string
    """


    PROJECT_NAME: Annotated[str, Field(default="Pragya's Momo Profit Predictor")]
    DEBUG: Annotated[bool, Field(default=True)]

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: Annotated[str, Field(default="localhost")]
    POSTGRES_PORT: Annotated[str, Field(default="5432")]

    MONGODB_URI: str
    MONGODB_DB: str

    @property
    def postgresql_url(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()