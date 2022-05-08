from typing import List, Dict
from fastapi import HTTPException


MAX_ELEMENTS_PER_REQUEST = 100000


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


def validate_time(from_time, to_time):
    if to_time < from_time:
        raise HTTPException(status_code=400, detail="'To time' cannot go before 'From time'")
    if from_time < 0:
        raise HTTPException(status_code=400, detail="Timestamp cannot be negative")


def validate_limit(limit):
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit should be greater than 0")


def validate_offset(offset):
    if offset < 0:
        raise HTTPException(status_code=400, detail="Offset should be greater or equal than 0")


async def get_number_of_news_in_region(collection, from_time, to_time):
    pipeline = [
        {"$match": {"published_timestamp": {"$gte": from_time, "$lte": to_time}}},
        {"$project": {"regions": {"$objectToArray": "$regions"}}},
        {"$unwind": "$regions"},
        {"$group": {"_id": "$regions.k", "count": {"$sum": 1}}},
    ]
    results = await collection.aggregate(pipeline).to_list(MAX_ELEMENTS_PER_REQUEST)
    return dict(zip([int(item["_id"]) for item in results],
                    [item["count"] for item in results]))


async def get_articles_in_region(collection, from_time, to_time, region, limit, offset):
    pipeline = [
        {"$match": {"published_timestamp": {"$gte": from_time, "$lte": to_time}}},
        {"$sort": {"published_timestamp": 1}},
        {"$project": {"regions": {"$objectToArray": "$regions"}}},
        {"$unwind": "$regions"},
        {"$match": {"regions.k": {"$eq": str(region)}}},
        {"$project": {"regions": 0}},
        {"$skip": offset},
        {"$limit": limit}
    ]
    result = await collection.aggregate(pipeline).to_list(MAX_ELEMENTS_PER_REQUEST)
    full_elements = await collection.find({"_id": {"$in": [elm["_id"] for elm in result]}})\
        .to_list(MAX_ELEMENTS_PER_REQUEST)

    for article in full_elements:
        article["confidence"] = article["regions"][str(region)]["confidence"]
        article["places"] = article["regions"][str(region)]["places"]
        del article["regions"]

    return full_elements
