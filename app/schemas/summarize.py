from pydantic import BaseModel
from typing import List, Optional

class SummarizeRequest(BaseModel):
    topic: str
    max_articles: Optional[int] = 5

class ActivityItem(BaseModel):
    title: str
    url: str

class SummarizeResponse(BaseModel):
    topic: str
    summary: str
    activities: List[ActivityItem]