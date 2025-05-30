from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import products, subscribers, users, payments

"""
Para lanzar el servidor: uvicorn main:app --reload --host 127.0.0.1 --port 8000
"""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(subscribers.router)
app.include_router(users.router)
app.include_router(payments.router)