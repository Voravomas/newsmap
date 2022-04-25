from typing import List, Dict


def aggregate_articles_by_regions(articles: List[dict]) -> Dict[int, List]:
    ret_dict = dict()
    for article in articles:
        if not article["regions"]:
            continue
        for region_num, article_region_details in article["regions"].items():
            if region_num not in ret_dict:
                ret_dict[region_num] = list()
            article_copy = dict(article)
            article_copy.pop("regions")
            article_copy.update(article_region_details)
            ret_dict[region_num].append(article_copy)
    return ret_dict
