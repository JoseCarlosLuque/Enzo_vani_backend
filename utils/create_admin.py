from pymongo import MongoClient
from passlib.context import CryptContext
from datetime import datetime

# Configuración de MongoDB
client = MongoClient("mongodb://localhost:27017")
db = client["Enzo_vani"]
users_collection = db["Users"]

# Configuración de hash de contraseña
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# === DATOS DEL NUEVO ADMIN ===
email = "admin@miapp.com"
password = "admin123"
role = "admin"

# === PROCESO ===
# Verifica si ya existe
existing_user = users_collection.find_one({"email": email})
if existing_user:
    print(f"❌ El usuario {email} ya existe en la base de datos.")
else:
    # Hashea la contraseña
    hashed_password = pwd_context.hash(password)

    # Inserta en MongoDB
    users_collection.insert_one({
        "email": email,
        "hashed_password": hashed_password,
        "role": role,
        "created_at": datetime.utcnow()
    })

    print(f"✅ Usuario admin {email} creado correctamente.")