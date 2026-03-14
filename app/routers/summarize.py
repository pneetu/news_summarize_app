from fastapi import APIRouter, HTTPException
from app.schemas.summarize import ActivitySummaryRequest, ActivitySummaryResponse
from app.services.summarize_service import summarize_activity_topic

router = APIRouter()

@router.post("/activity-summary", response_model= ActivitySummaryResponse)
async def summarize(req: ActivitySummaryRequest):
    try:
        result = await summarize_activity_topic(req.topic, req.max_articles)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))