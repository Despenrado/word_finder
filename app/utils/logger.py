import logging
import logging.config

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            # logging.FileHandler('app.log'),
            logging.StreamHandler()
        ]
    )

setup_logger()