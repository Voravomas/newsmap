"""
KW SEARCHER V1:

Rules:
1. All names of places should be capitalized
2. Article title is appended to article test
3. No villages
Answer:
1. If name of region then answer
2. If name from general then answer
3. If name of rayon then answer
4. If name of rayon without “ський район” then answer
5. If name of misto then answer

Keywords structure:
OBLAST = {
    "general": [str],
    "rayon": [str],
    "misto": [str],
    "selo": [str],
}
"""

from json import load
from typing import Optional


# BASE_RAYON_ENDING = "ький район"
BASE_RAYON_ENDING = "ький"

RAYON_SUFFICSES = ["iвс", "ївс", "ьсь", "ійс", "вс", "тс", "рс", "ц", "з",
                   ""  # last chance :^)
                   ]

SYMBOLS = [".", ",", "!", "?", ":", "-", "–"]

MINIMUM_CROPPED_RAYON_WORD = 4

KEYWORDS_LOCATION = "../misc/result2.json"


def download(path):
    with open(path, "r") as f:
        data = load(f)
    return data


def init_final(keys):
    fin_dict = dict()
    for obl in keys:
        fin_dict[obl] = {"num": 0, "exactly": []}
    return fin_dict


def inc(obl_name, value, fin_dict):
    fin_dict[obl_name]["num"] += 1
    fin_dict[obl_name]["exactly"].append(value)


def clear_emtpy(input_dict: dict):
    new_dict = dict()
    for k, w in input_dict.items():
        if w["num"] > 0:
            new_dict[k] = w
    return new_dict


def crop_rayon(rayon_name: str):
    for suffics in RAYON_SUFFICSES:
        cur_ending = suffics + BASE_RAYON_ENDING
        if rayon_name.endswith(cur_ending):
            rayon_cropped = rayon_name.split(cur_ending)[0]
            if len(rayon_cropped) >= MINIMUM_CROPPED_RAYON_WORD:
                return rayon_cropped
    return rayon_name


def leave_only_capitalized(text: str):
    filtered_text = []
    text = text.split()
    for word in text:
        word = word.strip()
        word = word.strip("\"")
        if not word:
            continue
        if any(char.isdigit() for char in word):
            continue
        if word[0].capitalize() != word[0]:
            continue
        for symbol in SYMBOLS:
            if word.endswith(symbol):
                word = word[:-1]
        if word.isnumeric():
            continue
        if word in SYMBOLS:
            continue
        if not word:
            continue
        word = word.strip("\"")
        filtered_text.append(word)
    return " ".join(filtered_text)


def kwsearcher(title: str, body: str, keywords: Optional[dict] = download(KEYWORDS_LOCATION)):
    answer = init_final(list(keywords.keys()))
    all_text = title + "\n" + body  # R2
    all_text = leave_only_capitalized(all_text)  # R3
    for oblast in keywords.keys():
        if oblast in all_text:  # A1
            inc(oblast, oblast, answer)
        for general_name in keywords[oblast]["general"]:
            if general_name in all_text:  # A2
                inc(oblast, general_name, answer)
        for rayon_name in keywords[oblast]["rayon"]:
            if rayon_name in all_text:  # A3
                inc(oblast, rayon_name, answer)
            if crop_rayon(rayon_name) in all_text:  # A4
                inc(oblast, rayon_name, answer)
        for misto_name in keywords[oblast]["misto"]:
            if misto_name in all_text:  # A5
                inc(oblast, misto_name, answer)
    return clear_emtpy(answer)
