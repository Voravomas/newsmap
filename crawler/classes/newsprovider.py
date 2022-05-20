import logging
from bs4 import BeautifulSoup
from copy import deepcopy
from time import sleep

from misc.common import make_request
from misc.constants import MAX_IDS_PER_NEWS_PROVIDER, TIMEOUT_BETWEEN_LINKS_REQUESTS
from misc.exceptions import PageProcessError
from .article import (PravdaArticle, EconomyPravdaArticle,
                      EuroPravdaArticle, LifePravdaArticle,
                      NVArticle, NVLifeArticle, NVBizArticle,
                      NVTechnoArticle, NVHealthArticle)


class NewsProvider:
    LINK_TO_ALL_ARTICLES = ""
    LINK_TO_CLASS_MAPPING = dict()

    @classmethod
    def fetch_new_links(cls, old_ids):
        logging.info("Fetching new links...")
        links = cls.get_all_links()
        logging.info(f"Got {len(links)} total links")
        ids_from_links = cls.links_to_ids(links)
        new_ids_filtered = cls.extract_new_ids(ids_from_links, old_ids)
        links_to_download = cls.get_links_to_download(new_ids_filtered, links)
        logging.info(f"Got {len(links_to_download)} NEW links after filtering")
        return new_ids_filtered, links_to_download

    @classmethod
    def get_all_links(cls):
        pass

    @classmethod
    def form_last_article_ids(cls, old_ids, new_ids):
        return (new_ids + old_ids)[:MAX_IDS_PER_NEWS_PROVIDER]

    @classmethod
    def extract_new_ids(cls, new_ids, old_ids):
        for old_id in old_ids:
            if old_id in new_ids:
                return new_ids[:new_ids.index(old_id)]
        return new_ids

    @classmethod
    def identify_article(cls, link):
        for article_link, article_type in cls.LINK_TO_CLASS_MAPPING.items():
            if link.startswith(article_link):
                return article_type
        return ""
        # raise Exception(f"Cannot identify type of article by link. Link: {link}")

    @classmethod
    def process(cls, old_ids):
        new_ids, new_links = cls.fetch_new_links(old_ids)
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
                raise PageProcessError(article_class.ARTICLE_TYPE, link, err)
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
    LINK_TO_CLASS_MAPPING = {
        "https://www.pravda.com.ua/": PravdaArticle,
        "https://www.epravda.com.ua/": EconomyPravdaArticle,
        "https://www.eurointegration.com.ua/": EuroPravdaArticle,
        "https://life.pravda.com.ua": LifePravdaArticle,
    }

    @classmethod
    def get_all_links(cls):
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

    @classmethod
    def links_to_ids(cls, links):
        return [link.split("/")[-2] for link in links]

    @classmethod
    def get_links_to_download(cls, ids, all_links):
        needed_links = []
        temp_ids = deepcopy(ids)
        for link in all_links:
            for single_id in temp_ids:
                formatted_id = f"/{single_id}/"
                if link.endswith(formatted_id):
                    needed_links.append(link)
                    temp_ids.remove(single_id)
                    break
        return needed_links


class NVNewsProvider(NewsProvider):
    BASE_LINK = "https://nv.ua/"
    LINK_TO_ALL_ARTICLES = BASE_LINK + "ukr/allnews.html"
    CLASS_OF_ALL_ARTICLES = "col-lg-9"
    CLASS_OF_ARTICLE = "row-result-body"
    LINK_TO_CLASS_MAPPING = {
        "https://nv.ua/": NVArticle,
        "https://biz.nv.ua/": NVLifeArticle,
        "https://techno.nv.ua/": NVBizArticle,
        "https://life.nv.ua/": NVTechnoArticle,
        "https://health.nv.ua/": NVHealthArticle
    }

    @classmethod
    def get_all_links(cls):
        links = []
        page = make_request(cls.LINK_TO_ALL_ARTICLES)
        soup = BeautifulSoup(page, 'html.parser')
        all_articles = soup.find_all("div", {"class": cls.CLASS_OF_ALL_ARTICLES})
        all_links = all_articles[0].findChildren("a", recursive=True)
        for link_obj in all_links:
            if link_obj.attrs['class'][0] == cls.CLASS_OF_ARTICLE:
                links.append(link_obj.attrs['href'])
        return links

    @classmethod
    def links_to_ids(cls, links):
        return [link.split("-")[-1].split(".html")[0] for link in links]

    @classmethod
    def get_links_to_download(cls, ids, all_links):
        needed_links = []
        for link in all_links:
            if link.split("-")[-1].split(".html")[0] in ids:
                needed_links.append(link)
        return needed_links


NEWS_PROVIDERS_MAPPING = {
    "Pravda": PravdaNewsProvider,
    "NV": NVNewsProvider
}
