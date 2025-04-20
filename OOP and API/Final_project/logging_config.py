import logging

def setup_logging():
    """
    Настройка логирования для приложения.
    Логи записываются в файл и выводятся в консоль.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("all_logs.log", encoding='utf-8'),  # Указываем кодировку utf-8
            logging.StreamHandler()  # Логи также будут выводиться в консоль
        ]
    )