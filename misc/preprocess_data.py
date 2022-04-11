# STRUCTURE
# NAME OF REGION: {GENERAL: [], RAYONS: [], MISTO/SELO: []}
# rayons {"R": , "F": }
from json import load, dump
from copy import deepcopy

PATH_RAW_JSON = "/Users/mykyta/aastudy/diploma/newsmap/UkraineCitiesAndVillages/CitiesAndVillages - 14 March.json"
EXPORT_PATH = "result2.json"

MISSING_CITIES = {
    "Дніпропетровська Область": ["Дніпропетровськ"],
    "Житомирська Область": ["Житомир"],
    "Запорізька Область": ["Запоріжжя"],
    "Київська Область": ["Київ"],
    "Кіровоградська Область": ["Кіровоград"],
    "Миколаївська Область": ["Миколаїв"],
    "Одеська Область": ["Одеса"],
    "Полтавська Область": ["Полтава"],
    "Сумська Область": ["Сумми"],
    "Харківська Область": ["Харків"],
    "Чернігівська Область": ["Чернігів"],
    "Автономна Республіка Крим": ["Крим"]
}

BASE_OBLAST = {
    "general": set(),
    "rayon": set(),
    "misto": set(),
    "selo": set(),
}

# {
#     "level_1": 100000000,
#     "level_2": 110100000,
#     "level_3": 110165600,
#     "level_4": "",
#     "object_category": "СМТ",
#     "object_name": "ГРЕСІВСЬКИЙ",
#     "object_code": 110165600,
#     "region": "АВТОНОМНА РЕСПУБЛІКА КРИМ",
#     "community": "СІМФЕРОПОЛЬСЬКИЙ РАЙОН"
#   },

SELO_TYPES = ["Селище", "СМТ", "Село"]

ENDINGS = [
    "ський",
    "цький"
]


def download(path):
    with open(path, "r") as f:
        data = load(f)
    return data


def upload(data):
    with open(EXPORT_PATH, "w", encoding='utf8') as f:
        dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)


def capitalize_full(word: str):
    if word.isalpha():
        fin_word = word.capitalize()
    elif word == 'М.СЕВАСТОПОЛЬ':
        fin_word = "Севастополь"
    elif " " in word:
        fin_word = " ".join([w.capitalize() for w in word.split(" ")])
    elif "-" in word:
        fin_word = "-".join([w.capitalize() for w in word.split("-")])
    elif "'" in word:
        fin_word = word.capitalize()
    else:
        raise Exception("CANNOT CAPITALIZE WORD: ", word)
    if fin_word.endswith("Район"):
        # fin_word = fin_word.replace("Район", "район")
        fin_word = fin_word.replace(" Район", "")
    return fin_word


def add_missing(input_dict: dict):
    for oblast, cities in MISSING_CITIES.items():
        input_dict[oblast]["general"].update(set(cities))

def main():
    processed_data = dict()
    raw_dict = download(PATH_RAW_JSON)
    for place in raw_dict:
        # creation of region base dict
        place_region = capitalize_full(place["region"])
        if place_region not in processed_data:
            processed_data[place_region] = deepcopy(BASE_OBLAST)

        if not place["community"].endswith("РАЙОН"):
            processed_data[place_region]["general"].add(capitalize_full(place["community"]))
        else:
            processed_data[place_region]["rayon"].add(capitalize_full(place["community"]))
            # cropped_rayon = crop_rayon(capitalize_full(place["community)"]))
            # processed_data[place_region]["rayon_cropped"].add(cropped_rayon)

        if place["object_category"] in SELO_TYPES:
            # processed_data[place_region]["selo"].add(capitalize_full(place["object_name"]))
            pass
        else:
            processed_data[place_region]["misto"].add(capitalize_full(place["object_name"]))

    add_missing(processed_data)

    for region_name in processed_data.keys():
        for k, w in processed_data[region_name].items():
            processed_data[region_name][k] = sorted(list(w))
    return processed_data


def tester():
    raw_dict = download(PATH_RAW_JSON)
    fin = set()
    for place in raw_dict:
        fin.add(place["region"])
    return fin






from pprint import pprint

# pprint(main())
upload(main())
# pprint(tester())
