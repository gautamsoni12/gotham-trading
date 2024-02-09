from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
from controller import stock, news
from bson import json_util
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/predictions")
def get_stock_predictions(
    max_results: int = 10, 
    filterValue: int = None,
    maxPrice: float = None,
    startDate: str = None,
    endDate: str = None
    ):
    predictions = stock.getStockPredictions(max_results, filterValue, maxPrice, startDate, endDate)
    return {
        "predictions": predictions
    }
    
@app.get("/stock")
def get_stock_info(
    symbol: str = None,
    ):
    stockData = stock.getStockData(symbol)
    
    return {
            "stockData": stockData
            }


@app.get("/financial/news")
def get_financial_news(
    date: str = None,
    ):
    news_result = news.get_daily_news(date)
    return news_result

@app.get("/prediction/result")
def get_prediction_result():
    prediction_result = stock.getPredictionResults()
    return prediction_result

if __name__ == "__main__":
   uvicorn.run("app:app", host='127.0.0.1', port=8000, log_level="info", reload=True)