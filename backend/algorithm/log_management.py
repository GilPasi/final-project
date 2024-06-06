import logging

def configure_logger(log_to_console: bool, log_level: str):

    logger = logging.getLogger('main_logger')
    
    level = getattr(logging, log_level.upper(), logging.DEBUG)
    logger.setLevel(level)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler('image_processing.log')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if log_to_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)


    if logger.hasHandlers():
        logger.handlers.clear()
        logger.addHandler(file_handler)
        if log_to_console:
            logger.addHandler(console_handler)

    return logger
