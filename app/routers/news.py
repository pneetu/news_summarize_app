from fastapi import APIRouter, Query
from activities import get_activity_data

router = APIRouter()

@router.get("/news")
async def get_news(
    limit: int = Query(default=2, ge=1, le=20),
    include_summary: bool = True
):
    data = get_activity_data(limit=limit, include_summary=include_summary)
    return data