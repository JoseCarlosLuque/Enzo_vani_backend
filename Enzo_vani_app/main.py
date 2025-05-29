from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

# CORS for React frontend 
# Configurado para que permita la comunicación con el servidor de desarrollo de React.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
# Para lanzar el server, situado en el directorio de main hacemos:  uvicorn main:app --reload --host 127.0.0.1 --port 8000
# Con el server corriendo se puede ir a http://localhost:8000/docs, y testear los endpoints.
client = MongoClient("mongodb://localhost:27017")
db = client["Enzo_vani"]
products_collection = db["Products"]
subscribers_collection = db["Subscribers"]

# Schemas
class Subscriber(BaseModel):
    email: EmailStr

class Product(BaseModel):
    name: str
    price: float
    stock: int
    image: str

@app.get("/products")
def get_products():
    products = []
    for product in products_collection.find():
        products.append({
            "id": str(product["_id"]),
            "name": product["name"],
            "image": product["image"],
            "price": product["price"],
            "stock": product["stock"]
        })
    return products

@app.post("/products")
def add_product(product: Product):
    result = products_collection.insert_one(product.dict())
    return {"message": "Producto añadido", "product_id": str(result.inserted_id)}

@app.get("/subscribers")
def get_subscribers():
    subscribers = []
    for subscriber in subscribers_collection.find():
        subscribers.append({
            "id": str(subscriber["_id"]),
            "email": subscriber["email"]
        })
    return subscriber

@app.post("/subscribe")
def subscribe(subscriber: Subscriber):
    existing = subscribers_collection.find_one({"email": subscriber.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email ya suscrito")
    subscribers_collection.insert_one({"email": subscriber.email})
    return {"message": f"¡Gracias por suscribirte, {subscriber.email}!"}
