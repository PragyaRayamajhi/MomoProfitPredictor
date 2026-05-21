from fastapi import APIRouter, Depends
from our_app.repositories.momo_repo import MomoRepository, get_momo_repo
from our_app.repositories.momo_mongo_repo import (
    MomoMongoRepository,
    get_momo_mongo_repo,
)
from our_app.services.v1.momo_service import create_prediction, predict_profit
from our_app.models.momo import MomoPredictionRequest, ProfitResult

router = APIRouter()


@router.post("/predict", response_model=ProfitResult)
async def predict(
    request: MomoPredictionRequest,
    repo: MomoRepository = Depends(get_momo_repo),
    mongo_repo: MomoMongoRepository = Depends(get_momo_mongo_repo),
):
    result = predict_profit(request)

    # Postgres: source-of-truth row
    await create_prediction(repo, request, result)

    # Mongo: flexible event log
    await mongo_repo.log_prediction(
        momo_type=request.momo_type,
        temperature=request.temperature,
        is_weekend=request.is_weekend,
        is_festival=request.is_festival,
        predicted_profit=result.predicted_profit_npr,
        recommendation=result.recommendation,
        confidence=result.confidence,
    )

    return result


@router.get("/history")
async def get_history(
    skip: int = 0,
    limit: int = 100,
    momo_type: str | None = None,
    repo: MomoRepository = Depends(get_momo_repo),
):
    records = await repo.get_all(skip=skip, limit=limit, momo_type=momo_type)
    return [
        {
            "id": r.id,
            "momo_type": r.momo_type,
            "temperature": r.temperature,
            "is_weekend": r.is_weekend,
            "is_festival": r.is_festival,
            "predicted_profit": r.predicted_profit,
            "recommendation": r.recommendation,
            "confidence": r.confidence,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]


@router.get("/logs")
async def get_logs(
    limit: int = 20,
    mongo_repo: MomoMongoRepository = Depends(get_momo_mongo_repo),
):
    return await mongo_repo.recent(limit=limit)


@router.get("/stats")
async def get_stats(
    mongo_repo: MomoMongoRepository = Depends(get_momo_mongo_repo),
):
    return {"mongo_prediction_count": await mongo_repo.count()}
