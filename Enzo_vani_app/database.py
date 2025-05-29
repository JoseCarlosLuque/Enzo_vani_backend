from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["Enzo_vani"]

products_collection = db["Products"]
subscribers_collection = db["Subscribers"]
users_collection = db["Users"]