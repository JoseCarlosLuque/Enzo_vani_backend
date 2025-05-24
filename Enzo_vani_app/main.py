from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017")
db = client["tienda"]
products_collection = db["products"]
subscribers_collection = db["subscribers"]

# Schemas
class Subscriber(BaseModel):
    email: EmailStr

@app.get("/products")
def get_products():
    products = []
    for product in products_collection.find():
        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "price": product["price"],
            "stock": product["stock"]
        })
    return products

@app.post("/subscribe")
def subscribe(subscriber: Subscriber):
    existing = subscribers_collection.find_one({"email": subscriber.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email ya suscrito")
    subscribers_collection.insert_one({"email": subscriber.email})
    return {"message": f"¡Gracias por suscribirte, {subscriber.email}!"}
