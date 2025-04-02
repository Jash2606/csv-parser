import os
from dotenv import load_dotenv

load_dotenv()
class Config:
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017')
    MONGO_DB = os.getenv('MONGO_DB', 'imdb_content')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    CACHE_TYPE = 'RedisCache'
    DEBUG = bool(os.getenv("DEBUG", False))
