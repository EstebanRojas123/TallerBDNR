from bson import ObjectId
from config.mongodb import mongo

def get_units_by_ids(unit_ids):
    # Devuelve todas las unidades que coincidan con los IDs dados
    units = list(mongo.db.unidad.find({"_id": {"$in": [ObjectId(unit_id) for unit_id in unit_ids]}}))
    
    # Convertir ObjectId a string para cada unidad
    for unit in units:
        unit["_id"] = str(unit["_id"])
    
    return units
