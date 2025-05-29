from fastapi import APIRouter, HTTPException, Depends
from models import User
from auth import get_password_hash, verify_password, create_access_token, get_current_user
from database import users_collection
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

router = APIRouter()

@router.post("/register")
def register(user: User):
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email ya registrado")
    hashed_password = get_password_hash(user.password)
    users_collection.insert_one({
        "email": user.email,
        "hashed_password": hashed_password,
        "created_at": datetime.utcnow()
    })
    return {"message": "Usuario registrado exitosamente"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Usuario no encontrado")
    if not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Contraseña incorrecta")
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=30)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def read_me(current_user: dict = Depends(get_current_user)):
    return {
        "email": current_user["email"],
        "created_at": current_user["created_at"]
    }
