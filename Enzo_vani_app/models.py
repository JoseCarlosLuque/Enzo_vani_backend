from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str

class Product(BaseModel):
    name: str
    price: float
    stock: int
    image: str

