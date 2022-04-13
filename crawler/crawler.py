from time import sleep

from classes.newsprovider import NEWS_PROVIDERS_MAPPING
from classes.database import Database
from misc.constants import TIMEOUT_SECONDS


def crawler(news_data: dict):
    article_data = dict()
    id_data = dict()
    for news_provider_name, news_provider_ids in news_data.items():
        ids, articles = NEWS_PROVIDERS_MAPPING[news_provider_name].process(news_provider_ids)
        article_data[news_provider_name] = articles
        id_data[news_provider_name] = ids
    return article_data, id_data


def main():
    client = Database.get_client()
    news_providers_data = Database.get_news_providers_data(client)
    article_data, id_data = crawler(news_providers_data)
    Database.load_article_data(client, article_data)
    Database.update_news_providers_ids(client, id_data)
    sleep(TIMEOUT_SECONDS)


if __name__ == '__main__':
    main()
