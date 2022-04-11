from bs4 import BeautifulSoup
from copy import deepcopy

from misc.common import make_request
from misc.constants import MAX_IDS_PER_NEWS_PROVIDER


class NewsProvider:
    @classmethod
    def fetch_new_links(cls, old_ids) -> bool:
        # make a request for all_pub_url
        # compare last article_id with collected last_article_id
        pass


class PravdaNewsProvider(NewsProvider):
    BASE_LINK = "https://www.pravda.com.ua"
    LINK_TO_ALL_ARTICLES = BASE_LINK + "/news/"
    CLASS_OF_ALL_ARTICLES = "container_sub_news_list_wrapper mode1"

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
    def extract_new_ids(cls, new_ids, old_ids):
        for old_id in old_ids:
            if old_id in new_ids:
                return new_ids[:new_ids.index(old_id)]
        return new_ids

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

    @classmethod
    def fetch_new_links(cls, old_ids):
        links = cls.get_all_links()
        ids_from_links = cls.links_to_ids(links)
        new_ids_filtered = cls.extract_new_ids(ids_from_links, old_ids)
        links_to_download = cls.get_links_to_download(new_ids_filtered, links)
        return links_to_download

    @classmethod
    def form_last_article_ids(cls, old_ids, new_ids):
        return (old_ids + new_ids)[:MAX_IDS_PER_NEWS_PROVIDER]
