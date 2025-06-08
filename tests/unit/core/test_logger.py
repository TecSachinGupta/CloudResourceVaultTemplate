from src.core import logger

def test_logger():
    log = logger.get_logger("test")
    log.info("Logger works!")
