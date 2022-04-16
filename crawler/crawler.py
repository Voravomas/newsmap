import logging
from time import sleep

from classes.newsprovider import NEWS_PROVIDERS_MAPPING
from classes.database import Database
from misc.constants import TIMEOUT_SECONDS


def crawler(news_data: dict):
    article_data = list()
    id_data = dict()
    for news_provider_name, news_provider_ids in news_data.items():
        logging.info(f"Start processing \"{news_provider_name}\"...")
        ids, articles = NEWS_PROVIDERS_MAPPING[news_provider_name].process(news_provider_ids)
        article_data += articles
        id_data[news_provider_name] = ids
        logging.info(f"Received {len(articles)} articles. Their names: {[article['title'] for article in articles]}")
        logging.info(f"Updated ids are: {ids}")
        logging.info(f"Finished processing \"{news_provider_name}\"")
    return article_data, id_data


def main():
    logging.basicConfig(format='[%(asctime)s] Message: %(message)s', level=logging.INFO)
    logging.info("The system has started")
    while True:
        client = Database.get_client()
        news_providers_data = Database.get_news_providers_data(client)
        logging.info("Executing crawler...")
        article_data, id_data = crawler(news_providers_data)
        logging.info("Crawler successfully executed")
        Database.load_article_data(client, article_data)
        Database.update_news_providers_ids(client, id_data)
        logging.info(f"Iteration succeeded.")
        logging.info(f"Sleeping {TIMEOUT_SECONDS} seconds...")
        sleep(TIMEOUT_SECONDS)


if __name__ == '__main__':
    main()
