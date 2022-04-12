from bs4 import BeautifulSoup
from datetime import datetime

from misc.kw_searcher_v1 import kwsearcher
from misc.common import make_request


class Article:
    @classmethod
    def get_beautiful_page(cls, link):
        pass

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
        pass


class PravdaArticle(Article):
    NEWS_PROVIDER_NAME = "Pravda"
    ARTICLE_TYPE = "Pravda"
    LANGUAGE = "UA"
    DATE_PUBLISHED_BLOCK_NAME = "post_time"
    TITLE_BLOCK_NAME = "post_title"
    TEXT_BODY_BLOCK_NAME = "post_text"
    TAGS_BLOCK_NAME = "post_tags"
    BODY_TAGS = ["p", "ul"]
    MONTH_DICT = {
        "січня": 1, "лютого": 2, "березня": 3, "квітня": 4, "травня": 5, "червня": 6,
        "липня": 7, "серпня": 8, "вересня": 9, "жовтня": 10, "листопада": 11, "грудня": 12
    }

    @classmethod
    def get_beautiful_page(cls, link):
        page_raw = make_request(link)
        return BeautifulSoup(page_raw, 'html.parser')

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
        if len(element[0].select("span.post_author")):
            element[0].select("span.post_author")[0].decompose()
        date_raw = str(element[0].contents[0])
        return cls.convert_date(date_raw)

    @classmethod
    def extract_title(cls, beautiful_page):
        element = beautiful_page.find_all("h1", {"class": cls.TITLE_BLOCK_NAME})
        title = str(element[0].contents[0])
        return title

    @classmethod
    def extract_text_body(cls, beautiful_page):
        elements_raw = beautiful_page.find_all("div", {"class": cls.TEXT_BODY_BLOCK_NAME})
        elements = []
        for tag_name in cls.BODY_TAGS:
            elements += elements_raw[0].findChildren(tag_name, recursive=False)
        elements_wo_tags = [' '.join(elm.stripped_strings) for elm in elements]
        return "\n".join(elements_wo_tags)

    @classmethod
    def extract_tags(cls, beautiful_page):
        element = beautiful_page.find_all("div", {"class": cls.TAGS_BLOCK_NAME})
        return list(element[0].stripped_strings)[1:]  # skipping "Теми: "

    @classmethod
    def get_page_data(cls, url):
        beautiful_page = cls.get_beautiful_page(url)
        date_published = cls.extract_date_published(beautiful_page)
        title = cls.extract_title(beautiful_page)
        body = cls.extract_text_body(beautiful_page)
        tags = cls.extract_tags(beautiful_page)
        return date_published, title, body, tags

    @classmethod
    def decompose_page_by_kw(cls, title, body, tags):
        return kwsearcher(title, body)

    @classmethod
    def to_json(cls, title, body, link, date_published, tags, regions):
        return {
            "title": title,
            "body": body,
            "news_provider_name": cls.NEWS_PROVIDER_NAME,
            "article_type": cls.ARTICLE_TYPE,
            "link": link,
            "time_published": date_published,
            "time_collected": str(datetime.now()),
            "text_language": cls.LANGUAGE,
            "tags": tags,
            "regions": regions
        }

    @classmethod
    def process(cls, link):
        date_published, title, body, tags = cls.get_beautiful_page(link)
        regions = cls.decompose_page_by_kw(title, body, tags)
        return cls.to_json(title, body, link, date_published, tags, regions)
