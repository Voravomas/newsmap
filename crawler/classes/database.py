import logging
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import List
from os import getenv

CONNECTION_STRING = getenv("CONNECTION_STRING")
DB_NAME = getenv("DB_NAME")
NEWS_PROVIDER_COLLECTION_NAME = getenv("NEWS_PROVIDER_COLLECTION_NAME")
ARTICLE_COLLECTION_NAME = getenv("ARTICLE_COLLECTION_NAME")

print("VARS ARE: ", CONNECTION_STRING, DB_NAME, NEWS_PROVIDER_COLLECTION_NAME, ARTICLE_COLLECTION_NAME)

if not DB_NAME or not CONNECTION_STRING\
        or not NEWS_PROVIDER_COLLECTION_NAME or not ARTICLE_COLLECTION_NAME:
    raise Exception("ENV variables are not set")


class Database:
    @classmethod
    def get_client(cls) -> MongoClient:
        logging.info("Getting a Mongo client...")
        mongo_client = MongoClient(CONNECTION_STRING)[DB_NAME]
        logging.info("Successfully got a Mongo client")
        return mongo_client

    @classmethod
    def get_collection(cls, client: MongoClient, collection_name: str) -> Collection:
        logging.info(f"Making a Mongo request for a collection: \"{collection_name}\"...")
        collection = client[collection_name]
        logging.info("Success")
        return collection

    @classmethod
    def load_documents(cls, client: MongoClient, documents: List[dict]) -> None:
        collection_name = ARTICLE_COLLECTION_NAME
        collection = cls.get_collection(client, collection_name)
        logging.info(f"Loading {len(documents)} documents to collection \"{collection_name}\"...")
        if documents:
            collection.insert_many(documents)
        logging.info("Success")

    @classmethod
    def get_news_providers_data(cls, client: MongoClient) -> dict:
        fin_dict = dict()
        collection = cls.get_collection(client, NEWS_PROVIDER_COLLECTION_NAME).find()
        logging.info("Getting news providers data...")
        collection_data = list(collection)
        for document in collection_data:
            fin_dict[document["news_provider_name"]] = document["news_provider_ids"]
        logging.info(f"News providers data is: {fin_dict}")
        return fin_dict

    @classmethod
    def update_news_providers_ids(cls, client: MongoClient, data: dict) -> None:
        collection = cls.get_collection(client, NEWS_PROVIDER_COLLECTION_NAME)
        logging.info("Updating news providers ids...")
        for news_provider_name, news_provider_ids in data.items():
            query = {"news_provider_name": news_provider_name}
            new_values = {"$set": {"news_provider_ids": news_provider_ids}}
            collection.update_one(query, new_values)
            logging.info(f"\"{news_provider_name}\" successfully updated")
