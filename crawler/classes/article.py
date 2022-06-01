from bs4 import BeautifulSoup
from datetime import datetime
from typing import Tuple, Optional

from misc.kw_searcher_v2 import kwsearcher
from misc.analyser import analyser
from misc.common import make_request, gen_random_str
from misc.constants import MONTH_DICT


class Article:
    NEWS_PROVIDER_NAME = ""
    ARTICLE_TYPE = ""
    LANGUAGE = "UA"

    @classmethod
    def convert_date(cls, date_raw: str) -> datetime:
        pass

    @classmethod
    def extract_date_published(cls, beautiful_page: BeautifulSoup) -> datetime:
        pass

    @classmethod
    def extract_title(cls, beautiful_page: BeautifulSoup) -> str:
        pass

    @classmethod
    def extract_text_body(cls, beautiful_page: BeautifulSoup) -> str:
        pass

    @classmethod
    def extract_tags(cls, beautiful_page: BeautifulSoup) -> list:
        pass

    @classmethod
    def link_to_id(cls, news_provider_name_raw: str, link_id: str) -> str:
        news_provider_name = news_provider_name_raw.lower().replace(' ', '_')
        return f"{news_provider_name}_{link_id}"

    @classmethod
    def get_beautiful_page(cls, link: str, headers: Optional[dict] = None) -> BeautifulSoup:
        page_raw = make_request(link, headers)
        return BeautifulSoup(page_raw, 'html.parser')

    @classmethod
    def decompose_page_by_kw(cls, title: str, body: str, tags: list) -> dict:
        kws = kwsearcher(f"{title}\n{body}")
        return analyser(kws, tags)

    @classmethod
    def get_page_data(cls, url: str) -> Tuple[datetime, str, str, list]:
        beautiful_page = cls.get_beautiful_page(url)
        date_published = cls.extract_date_published(beautiful_page)
        title = cls.extract_title(beautiful_page)
        body = cls.extract_text_body(beautiful_page)
        tags = cls.extract_tags(beautiful_page)
        return date_published, title, body, tags

    @classmethod
    def process(cls, link: str) -> dict:
        date_published, title, body, tags = cls.get_page_data(link)
        regions = cls.decompose_page_by_kw(title, body, tags)
        return cls.to_json(title, link, date_published, tags, regions)

    @classmethod
    def to_json(cls, title: str, link: str, date_published: datetime,
                tags: list, regions: dict) -> dict:
        return {
            "article_id": cls.link_to_id(cls.NEWS_PROVIDER_NAME, link),
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
    TEXT_BODY_BLOCK_TYPE = "div"
    DATE_PUBLISHED_BLOCK_NAME = ""
    AUTHOR_BLOCK_NAME = ""
    TITLE_BLOCK_NAME = ""
    TEXT_BODY_BLOCK_NAME = ""
    TAGS_BLOCK_NAME = ""

    @classmethod
    def link_to_id(cls, news_provider_name_raw: str, link: str) -> str:
        return Article.link_to_id(news_provider_name_raw, link.split("/")[-2])

    @classmethod
    def convert_date(cls, date_raw: str) -> datetime:
        _, date_published, time_published = date_raw.split(",")
        date_published = date_published.strip()
        day_num, month, year_num = date_published.split(" ")
        month_num = MONTH_DICT[month]
        hour_num, minutes_num = time_published.split(":")
        return datetime(int(year_num), month_num, int(day_num),
                        int(hour_num), int(minutes_num))

    @classmethod
    def extract_date_published(cls, beautiful_page: BeautifulSoup) -> datetime:
        element = beautiful_page.find_all("div",
                                          {"class": cls.DATE_PUBLISHED_BLOCK_NAME})
        # skipping author name
        if len(element[0].select(cls.AUTHOR_BLOCK_NAME)):
            element[0].select(cls.AUTHOR_BLOCK_NAME)[0].decompose()
        date_raw = str(element[0].contents[0])
        date_raw = date_raw.rstrip(" - ")
        return cls.convert_date(date_raw)

    @classmethod
    def extract_title(cls, beautiful_page: BeautifulSoup) -> str:
        titles = cls.TITLE_BLOCK_NAME
        titles = [titles] if isinstance(titles, str) else titles
        for title in titles:
            element = beautiful_page.find_all("h1", {"class": title})
            if element:
                break
        title = str(element[0].contents[0])
        return title

    @classmethod
    def extract_text_body(cls, beautiful_page: BeautifulSoup) -> str:
        elements_raw = beautiful_page.find_all(cls.TEXT_BODY_BLOCK_TYPE,
                                               {"class": cls.TEXT_BODY_BLOCK_NAME})
        elements = []
        for tag_name in cls.BODY_TAGS:
            elements += elements_raw[0].findChildren(tag_name, recursive=False)
        elements_wo_tags = [' '.join(elm.stripped_strings) for elm in elements]
        return "\n".join(elements_wo_tags)


class PravdaArticle(PravdaTypeArticle):
    ARTICLE_TYPE = "Pravda"
    AUTHOR_BLOCK_NAME = "span.post_author"
    DATE_PUBLISHED_BLOCK_NAME = "post_time"
    # Субота, 16 квітня 2022, 14:19
    TITLE_BLOCK_NAME = "post_title"
    TEXT_BODY_BLOCK_NAME = "post_text"
    TAGS_BLOCK_NAME = "post_tags"

    @classmethod
    def extract_tags(cls, beautiful_page: BeautifulSoup) -> list:
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
    def extract_tags(cls, beautiful_page: BeautifulSoup) -> list:
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
    def convert_date(cls, date_raw: str) -> datetime:
        # 15 квітня 2022
        day_num, month, year_num = date_raw.split(" ")
        month_num = MONTH_DICT[month]
        return datetime(int(year_num), month_num, int(day_num))

    @classmethod
    def extract_date_published(cls, beautiful_page: BeautifulSoup) -> datetime:
        element = beautiful_page.find_all("div",
                                          {"class": cls.DATE_PUBLISHED_BLOCK_NAME})
        date_raw = str(element[0].contents[1].string)
        return cls.convert_date(date_raw)

    @classmethod
    def extract_text_body(cls, beautiful_page: BeautifulSoup) -> str:
        fin_str = super().extract_text_body(beautiful_page)
        if cls.NOT_NEWS_STARTS_WITH in fin_str:
            idx = fin_str.index(cls.NOT_NEWS_STARTS_WITH)
            fin_str = fin_str[:idx]
        return fin_str

    @classmethod
    def extract_tags(cls, beautiful_page: BeautifulSoup) -> list:
        return []


class NVTypeArticle(Article):
    NEWS_PROVIDER_NAME = "NV"
    ARTICLE_TYPE = ""
    LANGUAGE = "UA"
    DATE_PUBLISHED_BLOCK_NAME = "article__head__additional_published"
    TEXT_BODY_BLOCK_NAME = "content_wrapper"
    TAGS_BLOCK_NAME = "article__tags"
    BODY_TAGS = ["p"]

    @classmethod
    def convert_date(cls, date_raw: str) -> datetime:
        # 20 травня, 08:30
        year = datetime.utcnow().year
        month_day, month, time_published = date_raw.split()
        month = MONTH_DICT[month[:-1]]  # ","
        hour, minute = time_published.split(":")
        return datetime(year, month, int(month_day), int(hour), int(minute))

    @classmethod
    def extract_date_published(cls, beautiful_page: BeautifulSoup) -> datetime:
        element = beautiful_page.find_all("div",
                                          {"class": cls.DATE_PUBLISHED_BLOCK_NAME})
        date_raw = str(element[0].contents[0].string)
        return cls.convert_date(date_raw)

    @classmethod
    def extract_title(cls, beautiful_page: BeautifulSoup) -> str:
        return str(beautiful_page.find_all("h1")[0].contents[0]).replace(chr(160), " ")

    @classmethod
    def extract_text_body(cls, beautiful_page: BeautifulSoup) -> str:
        # TODO: include to Article interface?
        elements_raw = beautiful_page.find_all("div",
                                               {"class": cls.TEXT_BODY_BLOCK_NAME})
        elements = []
        for tag_name in cls.BODY_TAGS:
            elements += elements_raw[0].findChildren(tag_name, recursive=True)
        elements_wo_tags = [' '.join(elm.stripped_strings) for elm in elements]
        return "\n".join(elements_wo_tags).replace(chr(160), " ")

    @classmethod
    def extract_tags(cls, beautiful_page: BeautifulSoup) -> list:
        element = beautiful_page.find_all("div", {"class": cls.TAGS_BLOCK_NAME})
        return list(element[0].stripped_strings)[1:]  # skipping "Теги: "

    @classmethod
    def link_to_id(cls, news_provider_name_raw: str, link: str) -> str:
        link_id = link.split("-")[-1].split(".html")[0]
        return Article.link_to_id(news_provider_name_raw, link_id)


class NVArticle(NVTypeArticle):
    ARTICLE_TYPE = "NV"


class NVLifeArticle(NVTypeArticle):
    ARTICLE_TYPE = "NVLife"


class NVBizArticle(NVTypeArticle):
    ARTICLE_TYPE = "NVBiz"


class NVTechnoArticle(NVTypeArticle):
    ARTICLE_TYPE = "NVTechno"


class NVHealthArticle(NVTypeArticle):
    ARTICLE_TYPE = "NVHealth"


class CensorNetArticle(Article):
    NEWS_PROVIDER_NAME = "CensorNet"
    ARTICLE_TYPE = "CensorNet"
    DATE_PUBLISHED_BLOCK_NAME = "g-time"
    LANGUAGE = "UA"
    TEXT_BODY_BLOCK_NAME = "news-text"
    BODY_TAGS = ["p"]
    TAGS_BLOCK_NAME = "news-tags"

    @classmethod
    def get_beautiful_page(cls, link: str, headers: Optional[dict] = None) -> BeautifulSoup:
        headers = {"User-Agent": gen_random_str(10)}
        return super().get_beautiful_page(link, headers)

    @classmethod
    def convert_date(cls, date_raw: str) -> datetime:
        # 21.05.22 18:47
        date_pub, time_pub = date_raw.split()
        d, mn, y = date_pub.split(".")
        h, mt = time_pub.split(":")
        return datetime(2000 + int(y), int(mn), int(d), int(h), int(mt))

    @classmethod
    def extract_date_published(cls, beautiful_page: BeautifulSoup) -> datetime:
        element = beautiful_page.find_all("time",
                                          {"class": cls.DATE_PUBLISHED_BLOCK_NAME})
        date_raw = str(element[0].contents[0].string).strip()
        return cls.convert_date(date_raw)

    @classmethod
    def extract_title(cls, beautiful_page: BeautifulSoup) -> str:
        return str(beautiful_page.find_all("h1")[0].contents[0]).replace(chr(160), " ").strip()

    @classmethod
    def extract_text_body(cls, beautiful_page: BeautifulSoup) -> str:
        elements_raw = beautiful_page.find_all("div",
                                               {"class": cls.TEXT_BODY_BLOCK_NAME})
        elements = []
        for tag_name in cls.BODY_TAGS:
            raw_elements = elements_raw[0].findChildren(tag_name, recursive=True)
            elements += [elm for elm in raw_elements if elm.get('class', [""])[0] != "related-news"]
        elements_wo_tags = [' '.join(elm.stripped_strings) for elm in elements]
        return "\n".join(elements_wo_tags).replace(chr(160), " ")

    @classmethod
    def extract_tags(cls, beautiful_page: BeautifulSoup) -> list:
        element = beautiful_page.find_all("div", {"class": cls.TAGS_BLOCK_NAME})
        raw_tags = list(element[0].stripped_strings)
        return [elm for elm in raw_tags if not elm.startswith("(")]  # skipping "(123)"

    @classmethod
    def link_to_id(cls, news_provider_name_raw: str, link: str) -> str:
        return Article.link_to_id(news_provider_name_raw, link.split("/")[5])
