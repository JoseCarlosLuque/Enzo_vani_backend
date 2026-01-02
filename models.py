from pydantic import BaseModel, EmailStr
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    password: str
    role: str

class Product(BaseModel):
    name: str
    price: float
    stock: int
    image: str

class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int

class Order(BaseModel):
    user_email: str
    items: List[OrderItem]
    total_amount: float
    status: str  # ej. "pending", "paid", "shipped"