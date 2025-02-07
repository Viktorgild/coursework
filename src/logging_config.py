import logging
import os


def setup_logger(name, log_file, level=logging.INFO):
    """Создание логгера с указанным именем и файлом."""
    # Убедитесь, что директория для логов существует
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Создание обработчика с указанием кодировки UTF-8
    handler = logging.FileHandler(log_file, encoding='utf-8')
    handler.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
