from config.mongodb import mongo
from flask import request, jsonify,Response
from bson import ObjectId, json_util
from services.units_service import get_units_by_ids

# Servicio para crear un curso completo con unidades y clases
def create_course_service():
    data = request.get_json()
    
    # Crear el curso básico sin unidades ni clases aún
    new_course = {
        "nombre": data["nombre"],
        "descripcion": data["descripcion"],
        "imagen_principal": data["imagen_principal"],
        "imagen_detalle": data["imagen_detalle"],
        "valoraciones": [],
        "valoracion_promedio": 0,
        "comentarios": [],
        "participantes": 0,
        "unidades": [],  # Esto se llenará después con los IDs de las unidades
        "inscritos": []  # Lista de IDs de usuarios inscritos, inicialmente vacía
    }
    
    # Insertar el curso en la colección 'curso' y obtener el ID
    course_id = mongo.db.curso.insert_one(new_course).inserted_id

    # Recorrer las unidades del JSON recibido y crear cada unidad
    unidades_ids = []
    for unidad in data["unidades"]:
        new_unit = {
            "nombre": unidad["nombre"],
            "orden": unidad["orden"],
            "curso_id": course_id,  # Asociar la unidad al curso
            "clases": []  # Esto se llenará con los IDs de las clases
        }
        
        unit_id = mongo.db.unidad.insert_one(new_unit).inserted_id
        unidades_ids.append(unit_id)

        clases_ids = []
        for clase in unidad["clases"]:
            new_class = {
                "nombre": clase["nombre"],
                "descripcion": clase["descripcion"],
                "video_url": clase["video_url"],
                "archivos_adjuntos": clase["archivos_adjuntos"],
                "orden": clase["orden"],
                "comentarios": [],
                "unidad_id": unit_id  # Asociar la clase a la unidad
            }

            class_id = mongo.db.clase.insert_one(new_class).inserted_id
            clases_ids.append(class_id)

        mongo.db.unidad.update_one(
            {"_id": unit_id},
            {"$set": {"clases": clases_ids}}
        )

    mongo.db.curso.update_one(
        {"_id": course_id},
        {"$set": {"unidades": unidades_ids}}
    )

    return jsonify({"message": "Curso creado exitosamente", "course_id": str(course_id)}), 201




def get_all_courses_service():

    courses = mongo.db.curso.find({}, {
        "nombre": 1,
        "imagen_principal": 1,
        "descripcion": 1,
        "valoracion_promedio": 1
    })
    
    course_list = []
    for course in courses:
        course["_id"] = str(course["_id"])  
        course_list.append(course)
    
    return jsonify({"cursos": course_list}), 200


def get_course_by_id(id):
    course = mongo.db.curso.find_one({"_id": ObjectId(id)})
    
    if course is None:
        return jsonify({"error": "Curso no encontrado"}), 404

    # Obtener unidades llamando al servicio
    unit_ids = course.get("unidades", [])
    course["unidades"] = get_units_by_ids(unit_ids)

    return Response(json_util.dumps(course), mimetype="application/json"), 200



def register_user_in_course(course_id, user_id):
    course = mongo.db.curso.find_one({"_id": ObjectId(course_id)})

    if not course:
        return jsonify({"error": "Curso no encontrado"}), 404


    if user_id in course.get("inscritos", []):
        return jsonify({"message": "Usuario ya está registrado en el curso"}), 200

    mongo.db.curso.update_one(
        {"_id": ObjectId(course_id)},
        {
            "$push": {"inscritos": user_id},
            "$inc": {"participantes": 1} 
        }
    )

    return jsonify({"message": "Usuario registrado correctamente"}), 200