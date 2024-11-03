from config.mongodb import mongo

def initialize_database():
    # Lista de colecciones que deseas crear
    collections = ['users', 'curso', 'unidad', 'clase', 'comentarios']

    for collection in collections:
        if collection not in mongo.db.list_collection_names():
            mongo.db.create_collection(collection)
            print(f"Creada colección: {collection}")
      
