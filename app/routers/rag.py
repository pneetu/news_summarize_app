from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from rag.rag_news import rag_answer

router = APIRouter()

class RagRequest(BaseModel):
    question: str
    top_k: int = 5

@router.post("/rag/answer")
async def rag_query(request: RagRequest):
    try:
        result = rag_answer(request.question, top_k=request.top_k)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))