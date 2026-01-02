from pymongo import MongoClient

# Conexión a MongoDB local
client = MongoClient('mongodb://localhost:27017/')

# Seleccionar base de datos y colección
db = client['Enzo_vani']
products_collection = db['Products']

# Lista de productos usando tus imágenes reales
products = [
    {
        "name": "Camiseta manga corta Enzo Vani",
        "image": "/camisetas_manga_corta.jpg",
        "price": 25.99,
        "stock": 40
    },
    {
        "name": "Camiseta manga corta diseño 2 Enzo Vani",
        "image": "/camisetas_manga_corta2.jpg",
        "price": 27.99,
        "stock": 35
    },
    {
        "name": "Camisa manga larga Enzo Vani",
        "image": "/camisas_manga_larga.jpg",
        "price": 45.99,
        "stock": 25
    },
    {
        "name": "Pantalón corto Enzo Vani",
        "image": "/pantalon_corto.jpg",
        "price": 32.99,
        "stock": 50
    },
    {
        "name": "Polo manga corta Enzo Vani",
        "image": "/Polos_manga_corta.jpg",
        "price": 29.99,
        "stock": 45
    },
    {
        "name": "Polo manga corta diseño 2 Enzo Vani",
        "image": "/Polos_manga_corta.jpg",
        "price": 31.99,
        "stock": 30
    },
    {
        "name": "Camiseta manga corta edición especial Enzo Vani",
        "image": "/camisetas_manga_corta.jpg",
        "price": 28.99,
        "stock": 20
    },
]

# Insertar productos y mostrar IDs generados
inserted = products_collection.insert_many(products)

print("Productos insertados con IDs:")
for _id in inserted.inserted_ids:
    print(str(_id))