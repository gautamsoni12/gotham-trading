from pymongo import MongoClient
from pydantic import BaseModel

# MongoDB connection settings
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "gotham_capital"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]


def save_to_mongo(item_to_save, collection_name):
    result = db[collection_name].insert_one(item_to_save)
    if result:
        return result
    else:
        return None
    
def get_from_mongo(query, collection_name):
    cursor = db[collection_name].find(query)
    result = [document for document in cursor]
    return result

def check_if_title_exists_in_collection(title: str, collection_name: str):
    result = db[collection_name].find_one({"title": title})
    return result is not None