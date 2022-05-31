class RetryableRequestError(Exception):
    pass


class NonRetryableRequestError(Exception):
    pass


class PageProcessError(Exception):
    def __init__(self, page_type, page_link, err):
        msg = f"An error occurred while processing a page from {page_type}. Page link: {page_link} Error: {err}"
        print(msg)
        raise
