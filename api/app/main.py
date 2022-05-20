import uvicorn
import motor.motor_asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asyncio import get_event_loop
from typing import List, Dict

from CREDENTIALS import CONNECTION_STRING, DB_NAME
from .models import ArticleModel, RegionRequest
from .utils import (validate_time, get_articles_in_region,
                   get_number_of_news_in_region, validate_limit, validate_offset)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = motor.motor_asyncio.AsyncIOMotorClient(CONNECTION_STRING)
client.get_io_loop = get_event_loop
db = client[DB_NAME]


@app.get("/")
async def read_root():
    return {"message": "It works!"}


@app.get(
    "/articles/total/{from_time}/{to_time}",
    response_description="Lists total number of articles per region",
    response_model=Dict[str, Dict[int, int]]
)
async def get_total_articles(from_time: int, to_time: int):
    validate_time(from_time, to_time)
    fin_dict = await get_number_of_news_in_region(db["articles"], from_time, to_time)
    return {"response": fin_dict}


@app.post(
    "/articles/",
    response_description="Lists articles by region and time period",
    response_model=Dict[str, List[ArticleModel]]
)
async def get_articles_by_region(request_data: RegionRequest):
    validate_time(request_data.from_time, request_data.to_time)
    validate_limit(request_data.limit)
    validate_offset(request_data.offset)

    data = await get_articles_in_region(db["articles"],
                                        request_data.from_time,
                                        request_data.to_time,
                                        request_data.region,
                                        request_data.limit,
                                        request_data.offset)
    return {"response": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
