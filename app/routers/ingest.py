from fastapi import APIRouter

router = APIRouter()

@router.get("/ingest-activities")
async def ingest_test():
    return {"status": "activity ingestion endpoint ready"}