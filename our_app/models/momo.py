# our_app/models/momo.py
from pydantic import BaseModel, Field
from typing import Literal

class MomoPredictionRequest(BaseModel):
    momo_type: Literal["BUFF", "CHICKEN", "VEG"] = Field(..., example="BUFF")
    temperature: float = Field(..., example=18.0)
    is_weekend: bool = Field(..., example=True)
    is_festival: bool = Field(False, example=True)

    class Config:
        from_attributes = True


class ProfitResult(BaseModel):
    predicted_profit_npr: float = Field(..., example=18500.0)
    recommendation: str = Field(..., example="Double BUFF production today!")
    confidence: Literal["High", "Medium", "Low"] = Field(..., example="High")

    class Config:
        from_attributes = True