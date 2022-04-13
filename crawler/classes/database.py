from pymongo import MongoClient
import pymongo

from CREDENTIALS import CONNECTION_STRING, DB_NAME

NEWS_PROVIDER_COLLECTION_NAME = "newsproviders"
ARTICLE_COLLECTION_NAME = "articles"


class Database:
    @classmethod
    def get_client(cls):
        return MongoClient(CONNECTION_STRING)[DB_NAME]

    @classmethod
    def get_collection(cls, client: MongoClient, collection_name):
        collection = client[collection_name]
        return collection

    @classmethod
    def load_documents(cls, client, collection_name, documents):
        collection = cls.get_collection(client, collection_name)
        collection.insert_many(documents)

    @classmethod
    def get_news_providers_data(cls, client):
        fin_dict = dict()
        collection = cls.get_collection(client, NEWS_PROVIDER_COLLECTION_NAME).find()
        collection_data = list(collection)
        for document in collection_data:
            fin_dict[document["news_provider_name"]] = document["news_provider_ids"]
        return fin_dict

    @classmethod
    def update_news_providers_ids(cls, client, data: dict):
        collection = cls.get_collection(client, NEWS_PROVIDER_COLLECTION_NAME)
        for news_provider_name, news_provider_ids in data.items():
            query = {"news_provider_name": news_provider_name}
            new_values = {"$set": {"news_provider_ids": news_provider_ids}}
            collection.update_one(query, new_values)

    @classmethod
    def load_article_data(cls, client, articles):
        return cls.load_documents(client, ARTICLE_COLLECTION_NAME, articles)

