import logging
from time import sleep
from typing import Tuple

from classes.newsprovider import NEWS_PROVIDERS_MAPPING
from classes.database import Database
from misc.constants import TIMEOUT_SECONDS


def crawler(news_data: dict) -> Tuple[list, dict]:
    article_data = list()
    id_data = dict()
    for news_provider_name, news_provider_ids in news_data.items():
        logging.info(f"Start processing \"{news_provider_name}\"...")
        ids, articles = NEWS_PROVIDERS_MAPPING[news_provider_name].process(news_provider_ids)
        article_data += articles
        id_data[news_provider_name] = ids
        logging.info(f"Received {len(articles)} articles. Their names: {[article['title'] for article in articles]}")
        logging.info(f"Updated ids are: {ids}")
        logging.info(f"Finished processing \"{news_provider_name}\"\n")
    return article_data, id_data


def sleep_but_awake(max_sleep):
    slept = 0
    sleep_step = 5
    while slept < max_sleep:
        sleep(sleep_step)
        slept += sleep_step
        logging.info(f"{slept}/{max_sleep}")


def main() -> None:
    logging.basicConfig(format='[%(asctime)s] Message: %(message)s', level=logging.INFO)
    logging.info("The system has started\n")
    while True:
        client = Database.get_client()
        news_providers_data = Database.get_news_providers_data(client)
        logging.info("Executing crawler...")
        article_data, id_data = crawler(news_providers_data)
        logging.info("Crawler successfully executed")
        Database.load_documents(client, article_data)
        Database.update_news_providers_ids(client, id_data)
        logging.info(f"Iteration succeeded.")
        logging.info(f"Sleeping {TIMEOUT_SECONDS} seconds...")
        sleep_but_awake(TIMEOUT_SECONDS)


if __name__ == '__main__':
    main()


# TODO: add -щина to oblasts
