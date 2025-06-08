import os

class Config:
    ENV = os.getenv("ENV", "dev")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
