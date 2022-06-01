from requests import get, RequestException
from backoff import on_exception, expo
from json import load
from os.path import dirname
from typing import Optional
from random import choice
from string import ascii_lowercase

from .exceptions import RetryableRequestError, NonRetryableRequestError
from .constants import MAX_RETRIES


def gen_random_str(length):
    return ''.join((choice(ascii_lowercase) for x in range(length)))


def _log_backoff(details: dict) -> None:
    print(f"Backing off {details['wait']:0.1f} seconds after {details['tries']} tries. "
          f"Request details: {details['args']} {details['kwargs']}")


def json_download(path: str) -> dict:
    with open(path, "r") as f:
        data = load(f)
    return data


def text_download(path: str) -> str:
    with open(path, "r") as f:
        data = f.read()
    return data


@on_exception(expo, RetryableRequestError,
              max_tries=MAX_RETRIES, on_backoff=_log_backoff)
def make_request(link: str, headers: Optional[dict] = None) -> str:
    response = None
    try:
        if headers:
            response = get(link, headers=headers)
        else:
            response = get(link)
        response.raise_for_status()
    except RequestException as err:
        response_error = "Unknown code"
        if response:
            response_error = response.status_code
        print(f"Got {response_error} error: {err}, response: {response}")
        if response.status_code > 500:
            raise RetryableRequestError()
        else:
            raise NonRetryableRequestError()
    return response.text


def get_path_to_project():
    cur_dir_path = dirname(__file__)
    str_end = cur_dir_path.rfind("newsmap") + len("newsmap")
    return cur_dir_path[:str_end]
