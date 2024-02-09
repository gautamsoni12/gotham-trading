from typing import List
from pydantic import BaseModel

class Topic(BaseModel):
    topic: str
    relevance_score: str

class NewsArticle(BaseModel):
    title: str
    url: str
    time_published: str
    authors: List[str]
    summary: str
    banner_image: str
    source: str
    category_within_source: str
    source_domain: str
    topics: List[dict]
    overall_sentiment_score: float
    overall_sentiment_label: str
    ticker_sentiment: List[object]