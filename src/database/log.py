import logging


def log_function_call(func):
    def wrapper(*args, **kwargs):
        logging.info(f"{func.__name__}({args})")
        return func(*args, **kwargs)

    return wrapper
