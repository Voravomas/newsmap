from .common import json_download, get_path_to_project

SYMBOLS = [".", ",", "!", "?", ":", "-", "–", "*", "/", "\\"]
# PATH_TO_PROJECT = get_path_to_project()
ALL_WORDS = set(json_download("crawler/misc/word_data/all_words.json")["words"])
WORD_CASES = json_download("crawler/misc/word_data/words_cases_to_main.json")
WORD_INFO = json_download("crawler/misc/word_data/word_info.json")


def leave_only_capitalized(text: str) -> list:
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
    return filtered_text


def lower_at_start(text: str) -> str:
    separators = ["\n", ".", "\""]
    lower_next = True
    fin_text = ""
    for symbol in text:
        if symbol in separators:
            lower_next = True
        if lower_next and symbol.isalpha():
            fin_text += symbol.lower()
            lower_next = False
            continue
        fin_text += symbol
    return fin_text


def add_double_word_cases(word_list: list) -> list:
    doubled_words = []
    if len(word_list) < 2:
        return word_list
    for idx in range(len(word_list) - 1):
        doubled_words.append(f"{word_list[idx]} {word_list[idx + 1]}")
    return word_list + doubled_words


def kwsearcher(title_and_body: str) -> list:
    fin_list = []
    words_with_capital_letters = leave_only_capitalized(lower_at_start(title_and_body))
    words_with_capital_letters = [word.lower() for word in words_with_capital_letters]
    actual_names = set(add_double_word_cases(words_with_capital_letters)).intersection(ALL_WORDS)
    for word in actual_names:
        word_in_prim_form_list = WORD_CASES[word]
        for word_in_prim_form in word_in_prim_form_list:
            word_info = WORD_INFO[word_in_prim_form]
            fin_list.append({"name": word_in_prim_form, "info": word_info})
    return fin_list
