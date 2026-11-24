import os


class Config:
    def __init__(self):
        self.APP_ENV = os.getenv("APP_ENV", "development")
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        self.PORT = int(os.getenv("PORT", "5000"))
        self.DEBUG = self.APP_ENV == "development"
