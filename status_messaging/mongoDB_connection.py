import pymongo
from mongoDB_config import config

myclient = pymongo.MongoClient(config["mongo_url"])
mydb = myclient[config["database_name"]]
mycol = mydb[config["collection_name"]]

print(f"Connected to {myclient}")
