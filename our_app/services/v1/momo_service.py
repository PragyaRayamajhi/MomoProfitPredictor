import random
from our_app.models.momo import MomoPredictionRequest, ProfitResult
from our_app.core.postgres import MomoProfitRecord
from our_app.repositories.momo_repo import MomoRepository

def predict_profit(request: MomoPredictionRequest) -> ProfitResult:
    base = 12000
    if request.momo_type == "BUFF": base += 8000
    if request.momo_type == "CHICKEN": base += 5000
    if request.is_weekend: base *= 1.8
    if request.is_festival: base *= 2.5
    temp_bonus = max(0, (20 - request.temperature) * 400)
    profit = base + temp_bonus + random.randint(800, 3000)

    confidence = "High" if request.temperature < 20 or request.is_festival else "Medium"
    recommendation = (
        "BUFF is on fire today!" if request.momo_type == "BUFF" and request.temperature < 18
        else "Festival rush incoming – go all out!" if request.is_festival
        else "Steady sales expected – keep it normal"
    )

    return ProfitResult(
        predicted_profit_npr=round(profit),
        recommendation=recommendation,
        confidence=confidence
    )

async def create_prediction(
    repo: MomoRepository,
    request: MomoPredictionRequest,
    result: ProfitResult
) -> MomoProfitRecord:
    record = MomoProfitRecord(
        momo_type=request.momo_type,
        temperature=request.temperature,
        is_weekend=request.is_weekend,
        is_festival=request.is_festival,
        predicted_profit=result.predicted_profit_npr,
        recommendation=result.recommendation,
        confidence=result.confidence,
    )
    return await repo.create(record)