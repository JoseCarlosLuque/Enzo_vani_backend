from pymongo import MongoClient
import config

#Cargamos la uri de Mongo desde el el arvhivo de configuracion.

client = MongoClient(config.mongo_uri)
db = client["Enzo_vani"]

products_collection = db["Products"]
subscribers_collection = db["Subscribers"]
users_collection = db["Users"]
orders_collection = db["Orders"]
