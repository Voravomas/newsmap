from bs4 import BeautifulSoup
from datetime import datetime

from misc.kw_searcher_v2 import kwsearcher
from misc.common import make_request


class Article:
    NEWS_PROVIDER_NAME = ""
    ARTICLE_TYPE = ""
    LANGUAGE = "UA"

    @classmethod
    def get_beautiful_page(cls, link):
        page_raw = make_request(link)
        return BeautifulSoup(page_raw, 'html.parser')

    @classmethod
    def convert_date(cls, date_raw):
        pass

    @classmethod
    def extract_date_published(cls, beautiful_page):
        pass

    @classmethod
    def extract_title(cls, beautiful_page):
        pass

    @classmethod
    def extract_text_body(cls, beautiful_page):
        pass

    @classmethod
    def extract_tags(cls, beautiful_page):
        pass

    @classmethod
    def get_page_data(cls, url):
        pass

    @classmethod
    def decompose_page_by_kw(cls, title, body, tags):
        title_and_body = f"{title}\n{body}"
        return kwsearcher(title_and_body)

    @classmethod
    def link_to_id(cls, link):
        pass

    @classmethod
    def to_json(cls, title, link, date_published, tags, regions):
        return {
            "id": cls.link_to_id(link),
            "title": title,
            "news_provider_name": cls.NEWS_PROVIDER_NAME,
            "article_type": cls.ARTICLE_TYPE,
            "link": link,
            "time_published": str(date_published),
            "published_timestamp": int(datetime.timestamp(date_published)),
            "time_collected": str(datetime.now()),
            "text_language": cls.LANGUAGE,
            "tags": tags,
            "regions": regions
        }


class PravdaTypeArticle(Article):
    NEWS_PROVIDER_NAME = "Pravda"
    BODY_TAGS = ["p", "ul", "h3"]
    MONTH_DICT = {
        "січня": 1, "лютого": 2, "березня": 3, "квітня": 4, "травня": 5, "червня": 6,
        "липня": 7, "серпня": 8, "вересня": 9, "жовтня": 10, "листопада": 11, "грудня": 12
    }
    TEXT_BODY_BLOCK_TYPE = "div"
    DATE_PUBLISHED_BLOCK_NAME = ""
    AUTHOR_BLOCK_NAME = ""
    TITLE_BLOCK_NAME = ""
    TEXT_BODY_BLOCK_NAME = ""
    TAGS_BLOCK_NAME = ""

    @classmethod
    def link_to_id(cls, link):
        return link.split("/")[-2]

    @classmethod
    def convert_date(cls, date_raw):
        _, date_published, time_published = date_raw.split(",")
        date_published = date_published.strip()
        day_num, month, year_num = date_published.split(" ")
        month_num = cls.MONTH_DICT[month]
        hour_num, minutes_num = time_published.split(":")
        return datetime(int(year_num), month_num, int(day_num),
                        int(hour_num), int(minutes_num))

    @classmethod
    def extract_date_published(cls, beautiful_page):
        element = beautiful_page.find_all("div", {"class": cls.DATE_PUBLISHED_BLOCK_NAME})
        # skipping author name
        if len(element[0].select(cls.AUTHOR_BLOCK_NAME)):
            element[0].select(cls.AUTHOR_BLOCK_NAME)[0].decompose()
        date_raw = str(element[0].contents[0])
        date_raw = date_raw.rstrip(" - ")
        return cls.convert_date(date_raw)

    @classmethod
    def extract_title(cls, beautiful_page):
        titles = [cls.TITLE_BLOCK_NAME] if isinstance(cls.TITLE_BLOCK_NAME, str) else cls.TITLE_BLOCK_NAME
        for title in titles:
            element = beautiful_page.find_all("h1", {"class": title})
            if element:
                break
        title = str(element[0].contents[0])
        return title

    @classmethod
    def extract_text_body(cls, beautiful_page):
        elements_raw = beautiful_page.find_all(cls.TEXT_BODY_BLOCK_TYPE, {"class": cls.TEXT_BODY_BLOCK_NAME})
        elements = []
        for tag_name in cls.BODY_TAGS:
            elements += elements_raw[0].findChildren(tag_name, recursive=False)
        elements_wo_tags = [' '.join(elm.stripped_strings) for elm in elements]
        return "\n".join(elements_wo_tags)

    @classmethod
    def get_page_data(cls, url):
        beautiful_page = cls.get_beautiful_page(url)
        date_published = cls.extract_date_published(beautiful_page)
        title = cls.extract_title(beautiful_page)
        body = cls.extract_text_body(beautiful_page)
        tags = cls.extract_tags(beautiful_page)
        return date_published, title, body, tags

    @classmethod
    def process(cls, link: str):
        date_published, title, body, tags = cls.get_page_data(link)
        regions = cls.decompose_page_by_kw(title, body, tags)
        return cls.to_json(title, link, date_published, tags, regions)


class PravdaArticle(PravdaTypeArticle):
    ARTICLE_TYPE = "Pravda"
    AUTHOR_BLOCK_NAME = "span.post_author"
    DATE_PUBLISHED_BLOCK_NAME = "post_time"
    # Субота, 16 квітня 2022, 14:19
    TITLE_BLOCK_NAME = "post_title"
    TEXT_BODY_BLOCK_NAME = "post_text"

    @classmethod
    def extract_tags(cls, beautiful_page):
        element = beautiful_page.find_all("div", {"class": cls.TAGS_BLOCK_NAME})
        return list(element[0].stripped_strings)[1:]  # skipping "Теми: "


class EconomyPravdaArticle(PravdaTypeArticle):
    ARTICLE_TYPE = "economyPravda"
    DATE_PUBLISHED_BLOCK_NAME = "post__time"
    AUTHOR_BLOCK_NAME = "span.post__author"
    TITLE_BLOCK_NAME = "post__title"
    TEXT_BODY_BLOCK_NAME = "post__text"
    TAGS_BLOCK_NAME = "post__tags"
    # Субота, 16 квітня 2022, 14:05

    @classmethod
    def extract_tags(cls, beautiful_page):
        element = beautiful_page.find_all("div", {"class": cls.TAGS_BLOCK_NAME})
        if not element:
            return []
        return list(element[0].stripped_strings)


class EuroPravdaArticle(EconomyPravdaArticle):
    ARTICLE_TYPE = "euroPravda"


class LifePravdaArticle(PravdaTypeArticle):
    NEWS_PROVIDER_NAME = "Pravda"
    ARTICLE_TYPE = "lifePravda"
    LANGUAGE = "UA"
    DATE_PUBLISHED_BLOCK_NAME = "data-block"
    TITLE_BLOCK_NAME = ["page-heading", "head"]
    TEXT_BODY_BLOCK_TYPE = "article"
    TEXT_BODY_BLOCK_NAME = "article"
    NOT_NEWS_STARTS_WITH = "Вас також може зацікавити:"

    @classmethod
    def convert_date(cls, date_raw):
        # 15 квітня 2022
        day_num, month, year_num = date_raw.split(" ")
        month_num = cls.MONTH_DICT[month]
        return datetime(int(year_num), month_num, int(day_num))

    @classmethod
    def extract_date_published(cls, beautiful_page):
        element = beautiful_page.find_all("div", {"class": cls.DATE_PUBLISHED_BLOCK_NAME})
        date_raw = str(element[0].contents[1].string)
        return cls.convert_date(date_raw)

    @classmethod
    def extract_text_body(cls, beautiful_page):
        fin_str = super().extract_text_body(beautiful_page)
        if cls.NOT_NEWS_STARTS_WITH in fin_str:
            idx = fin_str.index(cls.NOT_NEWS_STARTS_WITH)
            fin_str = fin_str[:idx]
        return fin_str

    @classmethod
    def extract_tags(cls, beautiful_page):
        return []
