import os

class Config:
    MONGO_CONNECTION = os.environ.get('MONGO_CONNECTION')
    DB_NAME = os.environ.get('DB_NAME')
    MONGO_URI = f"{os.environ.get('MONGO_CONNECTION')}/{os.environ.get('DB_NAME')}"