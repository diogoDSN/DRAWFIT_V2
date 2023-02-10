import logging
from os import environ

import drawfit.parameters as prm

def create_new_logger(name: str):
    logger = logging.getLogger(name)

    handler = logging.FileHandler('{}/{}.log'.format(environ['LOGS_PATH'], name))
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(levelname)s] - %(message)s', datefmt='%y/%m/%d %H:%M:%S'))
    logger.addHandler(handler)
    
    if prm.SHELL_MODE:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(levelname)s] - %(message)s', datefmt='%y/%m/%d %H:%M:%S'))
        logger.addHandler(handler)
    
    if prm.DEBUG_MODE:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    return logger
    