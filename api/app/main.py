import uvicorn
import motor.motor_asyncio
from fastapi import FastAPI, HTTPException
from asyncio import get_event_loop
from typing import List, Dict

from CREDENTIALS import CONNECTION_STRING, DB_NAME
from .models import ArticleModel
from .utils import aggregate_articles_by_regions


app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)
client.get_io_loop = get_event_loop
db = client[DB_NAME]


@app.get("/")
async def read_root():
    return {"message": "It works!"}


@app.get(
    "/articles/{from_time}/{to_time}",
    response_description="List articles by time and regions",
    response_model=Dict[int, List[ArticleModel]]
)
async def list_articles(from_time: int, to_time: int):
    if to_time < from_time:
        raise HTTPException(status_code=400, detail="'To time' cannot go before 'From time'")
    if from_time < 0:
        raise HTTPException(status_code=400, detail="Timestamp cannot be negative")
    articles = await db["articles"].find({"published_timestamp": {"$gte": from_time, "$lte": to_time}}).to_list(1000)  # TODO: implement batching
    return {"articles": aggregate_articles_by_regions(articles)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
