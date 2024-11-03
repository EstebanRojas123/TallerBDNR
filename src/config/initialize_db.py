from config.mongodb import mongo

def initialize_database():
    # Especifica la base de datos
    db = mongo.db.client["taller1"]
    
    # Lista de colecciones que deseas crear
    collections = ['users', 'curso', 'unidad', 'clase', 'comentarios']

    for collection in collections:
        if collection not in db.list_collection_names():
            # Crear la colección y un documento vacío temporal
            db[collection].insert_one({"_temp": "temp_data"})
            print(f"Creada colección: {collection}")
            # Elimina el documento temporal si no quieres que permanezca en la colección
            db[collection].delete_one({"_temp": "temp_data"})
