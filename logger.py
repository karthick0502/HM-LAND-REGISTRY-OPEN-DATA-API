import logging

def logger():
    # Logger Configuration
    logger = logging.getLogger()

    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)

        file_handler = logging.FileHandler("data_processing.log")
        console_handler = logging.StreamHandler()

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger