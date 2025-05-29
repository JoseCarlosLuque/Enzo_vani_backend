from fastapi import APIRouter
from database import products_collection

router = APIRouter()

@router.get("/products")
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

