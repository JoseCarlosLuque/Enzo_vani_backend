import os
from dotenv import load_dotenv
from pathlib import Path

def load_env():
    # Primero busca en el directorio donde se ejecuta el script
    env_path_root = Path(".") / ".env"
    env_path_app = Path(__file__).resolve().parent / ".env"

    if env_path_root.exists():
        load_dotenv(dotenv_path=env_path_root)
        print("✅ .env cargado desde raíz del proyecto")
    elif env_path_app.exists():
        load_dotenv(dotenv_path=env_path_app)
        print("✅ .env cargado desde carpeta Enzo_vani_app")
    else:
        print("⚠ No se encontró ningún archivo .env")


# Controlamos si las variables de entorno les llega en local o en el producción.
if os.getenv("ENV") != "production":
   load_env()

mongo_uri = os.getenv("MONGO_URI")
middleware_uri = os.getenv("MIDDLEWARE")
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
stripe_web_hook = os.getenv("STRIPE_WEBHOOK")
auth_secret_key = os.getenv("AUTH_SECRET_KEY")



