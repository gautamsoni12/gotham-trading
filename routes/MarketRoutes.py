from fastapi import APIRouter, HTTPException
from controller import market

router = APIRouter()

@router.post("/reddit/sentiment")
async def market_sentiment():
    try:
        marketSentimentResult = await market.marketSentiment()
        return marketSentimentResult
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))