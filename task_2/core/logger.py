import logging

from core import CONFIG


PATH = CONFIG.get('LOG_PATH')
LOG_FORMAT = (
    '%(asctime)s - %(name)s - %(levelname)s '
    '- %(funcName)s(%(lineno)d) - %(message)s'
)


def get_file_handler(name):
    file_handler = logging.FileHandler(f'{PATH}/{name}.log')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return file_handler


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler(name))
    logger.addHandler(get_stream_handler())
    return logger
