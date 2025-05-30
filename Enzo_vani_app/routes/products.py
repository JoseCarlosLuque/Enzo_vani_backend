from fastapi import APIRouter, Depends
from database import products_collection
from models import Product
from auth import get_current_admin_user
from fastapi import HTTPException
from bson import ObjectId

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


# ✅ Nuevo endpoint protegido solo para admins
@router.post("/admin/products")
async def create_product(
    product: Product,
    admin_user: dict = Depends(get_current_admin_user)
):
    new_product = {
        "name": product.name,
        "image": product.image,
        "price": product.price,
        "stock": product.stock
    }
    result = products_collection.insert_one(new_product)
    return {
        "message": "Producto creado exitosamente",
        "product_id": str(result.inserted_id)
    }


@router.delete("/admin/products/{product_id}")
async def delete_product(
    product_id: str,
    admin_user: dict = Depends(get_current_admin_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")

    result = products_collection.delete_one({"_id": ObjectId(product_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"message": f"Producto con ID {product_id} eliminado exitosamente"}
@router.put("/admin/products/{product_id}")
async def update_product(
    product_id: str,
    updated_product: Product,
    admin_user: dict = Depends(get_current_admin_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")

    update_data = {
        "name": updated_product.name,
        "price": updated_product.price,
        "stock": updated_product.stock,
        "image": updated_product.image
    }

    result = products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return {"message": f"Producto con ID {product_id} actualizado exitosamente"}