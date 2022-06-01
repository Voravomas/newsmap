import logging
from bs4 import BeautifulSoup
from time import sleep
from typing import Tuple, Union

from misc.common import make_request
from misc.constants import MAX_IDS_PER_NEWS_PROVIDER, TIMEOUT_BETWEEN_LINKS_REQUESTS, CENSOR_NET_HEADERS
from misc.exceptions import PageProcessError
from .article import (Article, PravdaArticle, EconomyPravdaArticle,
                      EuroPravdaArticle, LifePravdaArticle,
                      NVArticle, NVLifeArticle, NVBizArticle,
                      NVTechnoArticle, NVHealthArticle, CensorNetArticle)


class NewsProvider:
    LINK_TO_ALL_ARTICLES = ""
    LINK_TO_CLASS_MAPPING = dict()
    BASE_ARTICLE_CLASS = object

    @classmethod
    def get_all_links(cls):
        pass

    @classmethod
    def fetch_new_links(cls, old_ids: list) -> Tuple[list, list]:
        logging.info("Fetching new links...")
        links = cls.get_all_links()
        logging.info(f"Got {len(links)} total links")
        ids_from_links = cls.links_to_ids(links)
        new_ids_filtered = cls.extract_new_ids(ids_from_links, old_ids)
        links_to_download = cls.get_links_to_download(new_ids_filtered, links)
        logging.info(f"Got {len(links_to_download)} NEW links after filtering")
        return new_ids_filtered, links_to_download

    @classmethod
    def links_to_ids(cls, links: list) -> list:
        return [cls.BASE_ARTICLE_CLASS.link_to_id(cls.BASE_ARTICLE_CLASS.NEWS_PROVIDER_NAME, link) for link in links]

    @classmethod
    def get_links_to_download(cls, ids: list, all_links: list) -> list:
        needed_links = []
        for link in all_links:
            link_id = cls.BASE_ARTICLE_CLASS.link_to_id(cls.BASE_ARTICLE_CLASS.NEWS_PROVIDER_NAME, link)
            if link_id in ids:
                needed_links.append(link)
        return needed_links

    @classmethod
    def form_last_article_ids(cls, old_ids: list, new_ids: list) -> list:
        return (new_ids + old_ids)[:MAX_IDS_PER_NEWS_PROVIDER]

    @classmethod
    def extract_new_ids(cls, new_ids: list, old_ids: list) -> list:
        for old_id in old_ids:
            if old_id in new_ids:
                return new_ids[:new_ids.index(old_id)]
        return new_ids

    @classmethod
    def identify_article(cls, link: str) -> Union[str, Article]:
        for article_link, article_type in cls.LINK_TO_CLASS_MAPPING.items():
            if link.startswith(article_link):
                return article_type
        return ""

    @classmethod
    def process(cls, old_ids: list) -> Tuple[list, list]:
        try:
            new_ids, new_links = cls.fetch_new_links(old_ids)
        except Exception as err:
            logging.info(f"Skipping {cls.BASE_ARTICLE_CLASS.ARTICLE_TYPE} newsprovider"
                         f" because of error while requesting all links: {err}")
            return old_ids, []
        processed_articles = []
        updated_ids = cls.form_last_article_ids(old_ids, new_ids)

        for link in new_links:
            logging.info(f"Processing link: {link}")
            article_class = cls.identify_article(link)
            article_class_msg = article_class.ARTICLE_TYPE if article_class else 'None'
            logging.info(f"Article class: \"{article_class_msg}\"")
            if not article_class:
                logging.info(f"Skipping {link} link because it is not implemented yet")
                continue
            try:
                processed_article = article_class.process(link)
            except Exception as err:
                msg = "Page of type {} failed to proces. Link: {} is skipped because of error: {}"
                logging.info(msg.format(article_class.ARTICLE_TYPE, link, err))
                continue
            if not processed_article["regions"]:
                logging.info("Article is NOT added because no regions were found")
            else:
                logging.info("Article is added")
                processed_articles.append(processed_article)
            logging.info("Article successfully processed")
            logging.info(f"Sleeping {TIMEOUT_BETWEEN_LINKS_REQUESTS} seconds...\n")
            sleep(TIMEOUT_BETWEEN_LINKS_REQUESTS)

        return updated_ids, processed_articles


class PravdaNewsProvider(NewsProvider):
    BASE_LINK = "https://www.pravda.com.ua"
    LINK_TO_ALL_ARTICLES = BASE_LINK + "/news/"
    CLASS_OF_ALL_ARTICLES = "container_sub_news_list_wrapper mode1"
    BASE_ARTICLE_CLASS = PravdaArticle
    LINK_TO_CLASS_MAPPING = {
        "https://www.pravda.com.ua/": PravdaArticle,
        "https://www.epravda.com.ua/": EconomyPravdaArticle,
        "https://www.eurointegration.com.ua/": EuroPravdaArticle,
        "https://life.pravda.com.ua": LifePravdaArticle,
    }

    @classmethod
    def get_all_links(cls) -> list:
        links = []
        page = make_request(cls.LINK_TO_ALL_ARTICLES)
        soup = BeautifulSoup(page, 'html.parser')
        all_articles = soup.find_all("div", {"class": cls.CLASS_OF_ALL_ARTICLES})
        all_links = all_articles[0].findChildren("a", recursive=True)
        for link_obj in all_links:
            link = link_obj.attrs['href']
            if not link.startswith("http"):
                link = cls.BASE_LINK + link
            links.append(link)
        return links


class NVNewsProvider(NewsProvider):
    BASE_LINK = "https://nv.ua/"
    LINK_TO_ALL_ARTICLES = BASE_LINK + "ukr/allnews.html"
    CLASS_OF_ALL_ARTICLES = "col-lg-9"
    CLASS_OF_ARTICLE = "row-result-body"
    BASE_ARTICLE_CLASS = NVArticle
    LINK_TO_CLASS_MAPPING = {
        "https://nv.ua/": NVArticle,
        "https://biz.nv.ua/": NVBizArticle,
        "https://techno.nv.ua/": NVTechnoArticle,
        "https://life.nv.ua/": NVLifeArticle,
        "https://health.nv.ua/": NVHealthArticle
    }

    @classmethod
    def get_all_links(cls) -> list:
        links = []
        page = make_request(cls.LINK_TO_ALL_ARTICLES)
        soup = BeautifulSoup(page, 'html.parser')
        all_articles = soup.find_all("div", {"class": cls.CLASS_OF_ALL_ARTICLES})
        all_links = all_articles[0].findChildren("a", recursive=True)
        for link_obj in all_links:
            if link_obj.attrs['class'][0] == cls.CLASS_OF_ARTICLE:
                links.append(link_obj.attrs['href'])
        return links


class CensorNetNewsProvider(NewsProvider):
    BASE_LINK = "https://censor.net/"
    LINK_TO_ALL_ARTICLES = BASE_LINK + "ua/news/all"
    BASE_ARTICLE_CLASS = CensorNetArticle
    LINK_TO_CLASS_MAPPING = {
        "https://censor.net/": CensorNetArticle,
    }
    CLASS_OF_ALL_ARTICLES = "col-12 items-list"
    CLASS_OF_ARTICLE = "news-list-item__link"

    @classmethod
    def get_all_links(cls) -> list:
        links = []
        page = make_request(cls.LINK_TO_ALL_ARTICLES, CENSOR_NET_HEADERS)
        soup = BeautifulSoup(page, 'html.parser')
        all_articles = soup.find_all("div", {"class": cls.CLASS_OF_ALL_ARTICLES})
        all_links = all_articles[0].findChildren("a", recursive=True)
        for link_obj in all_links:
            if link_obj.attrs['class'][0] == cls.CLASS_OF_ARTICLE:
                links.append(link_obj.attrs['href'])
        return links


NEWS_PROVIDERS_MAPPING = {
    "Pravda": PravdaNewsProvider,
    "NV": NVNewsProvider,
    "CensorNet": CensorNetNewsProvider
}
