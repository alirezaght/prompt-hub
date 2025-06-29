import logging
logging.basicConfig(level=logging.INFO)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.

    :param name: The name of the logger.
    :return: A logging.Logger instance.
    """
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger