import logging

from drawfit.parameters import LOGS_PATH

DEBUG_MODE = False
SHELL_MODE = False



def create_new_logger(name: str):
    logger = logging.getLogger(name)
    
    handler = logging.FileHandler(f'{LOGS_PATH}/{name}.log')
    handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(levelname)s] - %(message)s', datefmt='%y/%m/%d %H:%M:%S'))
    logger.addHandler(handler)
    
    if SHELL_MODE:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(fmt='[%(asctime)s][%(levelname)s] - %(message)s', datefmt='%y/%m/%d %H:%M:%S'))
        logger.addHandler(handler)
    
    if DEBUG_MODE:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    return logger
    