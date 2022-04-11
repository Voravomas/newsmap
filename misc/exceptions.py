class RetryableRequestError(Exception):
    pass


class NonRetryableRequestError(Exception):
    pass
