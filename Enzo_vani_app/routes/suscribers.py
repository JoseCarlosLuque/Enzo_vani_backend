from fastapi import APIRouter, HTTPException
from pydantic import EmailStr
from database import subscribers_collection

router = APIRouter()

@router.post("/subscribe")
def subscribe(email: EmailStr):
    if subscribers_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email ya suscrito")
    subscribers_collection.insert_one({"email": email})
    return {"message": f"¡Gracias por suscribirte, {email}!"}