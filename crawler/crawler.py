from time import sleep

from classes.newsprovider import NEWS_PROVIDERS_MAPPING


def crawler(news_data: dict):
    processed_data = dict()
    for news_provider_name, news_provider_ids in news_data.items():
        ids, articles = NEWS_PROVIDERS_MAPPING[news_provider_name].process(news_provider_ids)
        processed_data[news_provider_name] = {"ids": ids,
                                              "articles": articles}
    return processed_data


def main():
    # TODO: connect to DB
    # TODO: extract news_provider_name, news_provider_ids from DB
    # TODO: execute crawler
    # TODO: load article_data to article
    # TODO: load ids to ids
    # TODO: sleep N minutes
    pass


if __name__ == '__main__':
    main()

