from pymongo import MongoClient

from core.config import DATABASE_NAME, MONGO_URI

if not MONGO_URI:
    raise RuntimeError("MONGO_URI must be configured before starting the API")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]