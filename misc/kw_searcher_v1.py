from json import load
from typing import Optional


BASE_RAYON_ENDING = "ький"

RAYON_SUFFICSES = ["iвс", "ївс", "ьсь", "ійс", "вс", "тс", "рс", "ц", "з",
                   ""  # last chance :^)
                   ]

SYMBOLS = [".", ",", "!", "?", ":", "-", "–"]

MINIMUM_CROPPED_RAYON_WORD = 4

KEYWORDS_LOCATION = "../misc/result2.json"


def download(path: str) -> str:
    with open(path, "r") as f:
        data = load(f)
    return data


def init_final(keys: list) -> dict:
    fin_dict = dict()
    for obl in keys:
        fin_dict[obl] = {"num": 0, "exactly": []}
    return fin_dict


def inc(obl_name: str, value: str, fin_dict: dict) -> None:
    fin_dict[obl_name]["num"] += 1
    fin_dict[obl_name]["exactly"].append(value)


def clear_emtpy(input_dict: dict) -> dict:
    new_dict = dict()
    for k, w in input_dict.items():
        if w["num"] > 0:
            new_dict[k] = w
    return new_dict


def crop_rayon(rayon_name: str) -> str:
    for suffices in RAYON_SUFFICSES:
        cur_ending = suffices + BASE_RAYON_ENDING
        if rayon_name.endswith(cur_ending):
            rayon_cropped = rayon_name.split(cur_ending)[0]
            if len(rayon_cropped) >= MINIMUM_CROPPED_RAYON_WORD:
                return rayon_cropped
    return rayon_name


def leave_only_capitalized(text: str) -> str:
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


def kwsearcher(title: str, body: str, keywords: Optional[dict] = download(KEYWORDS_LOCATION)) -> dict:
    answer = init_final(list(keywords.keys()))
    all_text = title + "\n" + body
    all_text = leave_only_capitalized(all_text)
    for oblast in keywords.keys():
        if oblast in all_text:
            inc(oblast, oblast, answer)
        for general_name in keywords[oblast]["general"]:
            if general_name in all_text:
                inc(oblast, general_name, answer)
        for rayon_name in keywords[oblast]["rayon"]:
            if rayon_name in all_text:
                inc(oblast, rayon_name, answer)
            if crop_rayon(rayon_name) in all_text:
                inc(oblast, rayon_name, answer)
        for misto_name in keywords[oblast]["misto"]:
            if misto_name in all_text:
                inc(oblast, misto_name, answer)
    return clear_emtpy(answer)
