from typing import List, Optional
from pydantic import BaseModel

class Topic(BaseModel):
    topic: str
    relevance_score: str

class RedditFeed(BaseModel):
    title: Optional[str]
    score: Optional[int]
    id: Optional[str]
    url: Optional[str]
    comms_num: Optional[int]
    created: Optional[float]
    body: Optional[str]