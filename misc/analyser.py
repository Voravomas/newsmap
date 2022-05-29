from copy import deepcopy
from typing import Union

from .constants import OBLAST_TO_NUM, OBLAST_BASE, CONFIDENCE_MAPPING
from .kw_searcher_v2 import WORD_INFO


def create_oblast_data_if_needed(num: str, dictionary: dict) -> None:
    if num not in dictionary:
        dictionary[num] = deepcopy(OBLAST_BASE)


def increment_oblast_confidence_if_needed(new_conf_rate: Union[float, int], oblast_data: dict) -> None:
    if oblast_data["confidence"] < new_conf_rate:
        oblast_data["confidence"] = new_conf_rate


def post_process(input_dict: dict) -> None:
    for item, value in input_dict.items():
        value["places"] = sorted(list(value["places"]))


def analyser(keywords: list, tags: list) -> dict:
    fin_dict = dict()
    for tag in tags:
        if tag in OBLAST_TO_NUM:
            create_oblast_data_if_needed(OBLAST_TO_NUM[tag], fin_dict)
            fin_dict[OBLAST_TO_NUM[tag]]["confidence"] = 1
            fin_dict[OBLAST_TO_NUM[tag]]["places"].add(tag)
        if tag in WORD_INFO:
            tag_data = WORD_INFO[tag]
            for place in tag_data:
                create_oblast_data_if_needed(place["oblast"], fin_dict)
                increment_oblast_confidence_if_needed(CONFIDENCE_MAPPING[place["type"]], fin_dict[place["oblast"]])
                fin_dict[place["oblast"]]["places"].add(tag)

    for keyword in keywords:
        for place in keyword["info"]:
            create_oblast_data_if_needed(place["oblast"], fin_dict)
            increment_oblast_confidence_if_needed(CONFIDENCE_MAPPING[place["type"]], fin_dict[place["oblast"]])
            fin_dict[place["oblast"]]["places"].add(keyword["name"])
    post_process(fin_dict)
    return fin_dict
