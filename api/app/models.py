from bson import ObjectId
from typing import List
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class ArticleModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    article_id: str = Field(...)
    title: str = Field(...)
    news_provider_name: str = Field(...)
    article_type: str = Field(...)
    link: str = Field(...)
    time_published: str = Field(...)
    published_timestamp: int = Field(...)
    time_collected: str = Field(...)
    text_language: str = Field(...)
    tags: List[str] = Field(...)
    confidence: float = Field(...)
    places: List[str] = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
               "article_id": "7340475",
               "title": "Ле Пен після війни в Україні готова взаємодіяти з РФ, щоб запобігти її альянсу з Китаєм",
               "news_provider_name": "Pravda",
               "article_type": "Pravda",
               "link": "https://www.pravda.com.ua/news/2022/04/18/7340475/",
               "time_published": "2022-04-18 17:42:00",
               "published_timestamp": 1650292920,
               "time_collected": "2022-04-18 17:59:08.279164",
               "text_language": "UA",
               "tags": ["Ле Пен", "Львівська область"],
               "confidence": 0.5,
               "places": ["Львів", "Самбір"]
            }
        }
