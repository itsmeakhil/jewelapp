import logging
from logging.handlers import RotatingFileHandler

# create a logging format
from utils.utils import log_file_exists

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def info(message):
    logger = logging.getLogger('HomeSafe-INFO')
    logger.setLevel(logging.INFO)
    filename = 'logs/info/info.log'
    log_file_exists(filename)
    handler = RotatingFileHandler(filename, maxBytes=20000, backupCount=100)
    console = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.info(message)


def debug(message):
    logger = logging.getLogger('HomeSafe-DEBUG')
    logger.setLevel(logging.DEBUG)
    filename = 'logs/debug/debug.log'
    log_file_exists(filename)
    handler = RotatingFileHandler(filename, maxBytes=20000, backupCount=100)
    console = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.debug(message)


def warning(message):
    logger = logging.getLogger('HomeSafe-WARNING')
    logger.setLevel(logging.WARNING)
    filename = 'logs/warning/warning.log'
    log_file_exists(filename)
    handler = RotatingFileHandler(filename, maxBytes=20000, backupCount=100)
    console = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.warning(message)


def error(message):
    logger = logging.getLogger('HomeSafe-ERROR')
    logger.setLevel(logging.ERROR)
    filename = 'logs/error/error.log'
    log_file_exists(filename)
    handler = RotatingFileHandler(filename, maxBytes=20000, backupCount=100)
    console = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.error(message)
