from bson import ObjectId
from flask import jsonify,request
from config.mongodb import mongo
import requests

def get_units_by_ids(unit_ids):
    units = list(mongo.db.unidad.find({"_id": {"$in": [ObjectId(unit_id) for unit_id in unit_ids]}}))
    
  
    for unit in units:
        unit["_id"] = str(unit["_id"])
    
        return units



def get_classes_by_unit_id(unit_id):
    unit = mongo.db.unidad.find_one({"_id": ObjectId(unit_id)}, {"clases": 1})
    
    if not unit:
        return jsonify({"error": "Unidad no encontrada"}), 404


    class_ids = unit.get("clases", [])


    classes = list(mongo.db.clase.find(
        {"_id": {"$in": [ObjectId(class_id) for class_id in class_ids]}},
        {"nombre": 1}
    ))

    for cls in classes:
        cls["_id"] = str(cls["_id"])

    return jsonify({"clases": classes}), 200



def add_course_rating_service(course_id):
    # Obtener la valoración desde el cuerpo de la solicitud
    data = request.get_json()
    valoracion = data.get("valoracion")

    # Validar que la valoración esté presente y sea un número válido
    if valoracion is None or not isinstance(valoracion, (int, float)) or not (0 <= valoracion <= 5):
        return jsonify({"error": "La valoración debe ser un número entre 0 y 5."}), 400

    # Buscar el curso por ID
    course = mongo.db.curso.find_one({"_id": ObjectId(course_id)})

    if not course:
        return jsonify({"error": "Curso no encontrado."}), 404

    # Agregar la valoración al array 'valoraciones'
    mongo.db.curso.update_one(
        {"_id": ObjectId(course_id)},
        {"$push": {"valoraciones": valoracion}}
    )

    # Recalcular la valoración promedio
    valoraciones_actualizadas = course.get("valoraciones", []) + [valoracion]
    valoracion_promedio = sum(valoraciones_actualizadas) / len(valoraciones_actualizadas)

    # Actualizar la valoración promedio en la base de datos
    mongo.db.curso.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": {"valoracion_promedio": valoracion_promedio}}
    )

    return jsonify({"message": "Valoración agregada correctamente.", "valoracion_promedio": valoracion_promedio}), 200