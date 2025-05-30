from pydantic import BaseModel, EmailStr

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

