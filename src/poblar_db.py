from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from dotenv import load_dotenv
from config.mongodb import mongo
from bson.objectid import ObjectId
import os

# Cargar variables de entorno desde el archivo .env
#load_dotenv()

# Obtener la URI de MongoDB desde la variable de entorno
#MONGO_URI = os.getenv("MONGO_URI")

# Conectar a la base de datos en la nube usando la URI obtenida
#client = MongoClient(MONGO_URI)
#db = client['taller1']  # Reemplaza 'DB' con el nombre de tu base de datos

def clear_database():
    """Opcional: Limpia las colecciones antes de poblar para evitar duplicados."""
    mongo.db.users.delete_many({})
    mongo.db.curso.delete_many({})
    mongo.db.unidad.delete_many({})
    mongo.db.clase.delete_many({})
    mongo.db.comentarios.delete_many({})
    print("Colecciones limpiadas.")

def populate_users():
    """Inserta usuarios de ejemplo en la colección 'users'."""
    users = [
        {"username": "admin", "password": "admin123", "admin": True},
        {"username": "user1", "password": "password1", "admin": False},
        {"username": "user2", "password": "password2", "admin": False},
        {"username": "user3", "password": "password3", "admin": False},
        {"username": "user4", "password": "password4", "admin": False},
        {"username": "user5", "password": "password5", "admin": False}
    ]
    result = mongo.db.users.insert_many(users)
    user_ids = result.inserted_ids
    print(f"Usuarios insertados con IDs: {user_ids}")
    return user_ids

def populate_courses(user_ids):
    """Inserta 5 cursos con sus unidades y clases."""
    cursos = [
        {
            "nombre": "Aprende a Jugar LOL",
            "descripcion": "Curso completo para aprender League of Legends desde cero.",
            "imagen_principal": "lol_principal.jpg",
            "imagen_detalle": "lol_detalle.jpg",
            "valoraciones": [],
            "valoracion_promedio": 0,
            "comentarios": [],
            "participantes": 0,
            "inscritos": [],
            "unidades": []
        },
        {
            "nombre": "Desarrollo Web con Flask",
            "descripcion": "Curso intensivo para desarrollar aplicaciones web usando Flask.",
            "imagen_principal": "flask_principal.jpg",
            "imagen_detalle": "flask_detalle.jpg",
            "valoraciones": [],
            "valoracion_promedio": 0,
            "comentarios": [],
            "participantes": 0,
            "inscritos": [],
            "unidades": []
        },
        {
            "nombre": "Introducción a la Inteligencia Artificial",
            "descripcion": "Aprende los fundamentos de la IA y sus aplicaciones.",
            "imagen_principal": "ia_principal.jpg",
            "imagen_detalle": "ia_detalle.jpg",
            "valoraciones": [],
            "valoracion_promedio": 0,
            "comentarios": [],
            "participantes": 0,
            "inscritos": [],
            "unidades": []
        },
        {
            "nombre": "Bases de Datos con MongoDB",
            "descripcion": "Curso completo sobre el manejo de bases de datos NoSQL con MongoDB.",
            "imagen_principal": "mongodb_principal.jpg",
            "imagen_detalle": "mongodb_detalle.jpg",
            "valoraciones": [],
            "valoracion_promedio": 0,
            "comentarios": [],
            "participantes": 0,
            "inscritos": [],
            "unidades": []
        },
        {
            "nombre": "Desarrollo de Videojuegos con Unity",
            "descripcion": "Aprende a crear videojuegos desde cero usando Unity.",
            "imagen_principal": "unity_principal.jpg",
            "imagen_detalle": "unity_detalle.jpg",
            "valoraciones": [],
            "valoracion_promedio": 0,
            "comentarios": [],
            "participantes": 0,
            "inscritos": [],
            "unidades": []
        }
    ]

    curso_ids = []
    for curso in cursos:
        curso_id = mongo.db.curso.insert_one(curso).inserted_id
        curso_ids.append(curso_id)
        print(f"Curso '{curso['nombre']}' insertado con ID: {curso_id}")
    return curso_ids

def populate_units(curso_ids):
    """Inserta unidades para cada curso."""
    unidades_data = {
        "Aprende a Jugar LOL": [
            {"nombre": "Fundamentos de LOL", "orden": 1},
            {"nombre": "Estrategias Avanzadas", "orden": 2}
        ],
        "Desarrollo Web con Flask": [
            {"nombre": "Introducción a Flask", "orden": 1},
            {"nombre": "Bases de Datos con Flask", "orden": 2},
            {"nombre": "Despliegue de Aplicaciones", "orden": 3}
        ],
        "Introducción a la Inteligencia Artificial": [
            {"nombre": "Conceptos Básicos de IA", "orden": 1},
            {"nombre": "Aprendizaje Automático", "orden": 2},
            {"nombre": "Redes Neuronales", "orden": 3}
        ],
        "Bases de Datos con MongoDB": [
            {"nombre": "Introducción a MongoDB", "orden": 1},
            {"nombre": "Operaciones CRUD", "orden": 2},
            {"nombre": "Agregaciones y Consultas Avanzadas", "orden": 3}
        ],
        "Desarrollo de Videojuegos con Unity": [
            {"nombre": "Fundamentos de Unity", "orden": 1},
            {"nombre": "Creación de Personajes", "orden": 2},
            {"nombre": "Programación en C#", "orden": 3},
            {"nombre": "Publicación de Juegos", "orden": 4}
        ]
    }

    unidad_ids = {}
    for curso_id in curso_ids:
        curso = mongo.db.curso.find_one({"_id": curso_id})
        curso_nombre = curso["nombre"]
        unidades = unidades_data.get(curso_nombre, [])
        inserted_unidades = []
        for unidad in unidades:
            unidad_document = {
                "nombre": unidad["nombre"],
                "orden": unidad["orden"],
                "curso_id": curso_id,
                "clases": []
            }
            unidad_id = mongo.db.unidad.insert_one(unidad_document).inserted_id
            inserted_unidades.append(unidad_id)
            print(f"Unidad '{unidad['nombre']}' insertada con ID: {unidad_id} para el curso '{curso_nombre}'")
        # Actualizar el curso con las unidades
        mongo.db.curso.update_one({"_id": curso_id}, {"$set": {"unidades": inserted_unidades}})
        unidad_ids[curso_nombre] = inserted_unidades
    return unidad_ids

def populate_classes(unidad_ids):
    """Inserta clases para cada unidad."""
    clases_data = {
        "Fundamentos de LOL": [
            {
                "nombre": "Introducción a los Campeones",
                "descripcion": "Conoce los diferentes campeones y sus roles.",
                "video_url": "https://youtube.com/introduccion_campeones.mp4",
                "archivos_adjuntos": ["campeones.pdf"],
                "orden": 1
            },
            {
                "nombre": "Mapas y Objetivos",
                "descripcion": "Aprende sobre los mapas y los objetivos clave.",
                "video_url": "https://youtube.com/mapas_objetivos.mp4",
                "archivos_adjuntos": ["mapas.pdf"],
                "orden": 2
            }
        ],
        "Estrategias Avanzadas": [
            {
                "nombre": "Control de Visión",
                "descripcion": "Técnicas para controlar la visión del mapa.",
                "video_url": "https://youtube.com/control_vision.mp4",
                "archivos_adjuntos": ["vision.pdf"],
                "orden": 1
            },
            {
                "nombre": "Rotaciones y Posicionamiento",
                "descripcion": "Mejora tus rotaciones y posicionamiento en el juego.",
                "video_url": "https://youtube.com/rotaciones_posicionamiento.mp4",
                "archivos_adjuntos": ["rotaciones.pdf"],
                "orden": 2
            }
        ],
        "Introducción a Flask": [
            {
                "nombre": "Configuración del Entorno",
                "descripcion": "Instalación y configuración de Flask.",
                "video_url": "https://youtube.com/configuracion_flask.mp4",
                "archivos_adjuntos": ["instalacion.pdf"],
                "orden": 1
            },
            {
                "nombre": "Rutas y Vistas",
                "descripcion": "Creación de rutas y vistas en Flask.",
                "video_url": "https://youtube.com/rutas_vistas.mp4",
                "archivos_adjuntos": ["rutas.pdf"],
                "orden": 2
            }
        ],
        # Agrega más clases para las demás unidades según sea necesario
    }

    for curso_nombre, unidades in unidad_ids.items():
        for unidad_id in unidades:
            unidad = mongo.db.unidad.find_one({"_id": unidad_id})
            unidad_nombre = unidad["nombre"]
            clases = clases_data.get(unidad_nombre, [])
            if not clases:
                continue  # Salta si no hay clases definidas para esta unidad
            clases_ids = []
            for clase in clases:
                clase_document = {
                    "nombre": clase["nombre"],
                    "descripcion": clase["descripcion"],
                    "video_url": clase["video_url"],
                    "archivos_adjuntos": clase["archivos_adjuntos"],
                    "orden": clase["orden"],
                    "comentarios": [],
                    "unidad_id": unidad_id
                }
                clase_id = mongo.db.clase.insert_one(clase_document).inserted_id
                clases_ids.append(clase_id)
                print(f"Clase '{clase['nombre']}' insertada con ID: {clase_id} para la unidad '{unidad_nombre}'")
            # Actualizar la unidad con las clases
            mongo.db.unidad.update_one({"_id": unidad_id}, {"$set": {"clases": clases_ids}})

def populate_comments(user_ids, curso_ids, unidad_ids):
    """Inserta comentarios para algunos cursos y clases."""
    import random
    selected_users = random.sample(user_ids, 3)  # Selecciona 3 usuarios

    comentarios_curso = [
        {
            "title": "Excelente Curso",
            "id_user": str(selected_users[0]),
            "content": "He aprendido mucho sobre League of Legends.",
            "likes": 15,
            "dislikes": 1,
            "fecha": datetime.utcnow(),
            "entity_type": "curso",
            "entity_id": str(curso_ids[0])
        },
        {
            "title": "Muy útil",
            "id_user": str(selected_users[1]),
            "content": "El curso de Flask me ha ayudado a desarrollar aplicaciones web rápidamente.",
            "likes": 10,
            "dislikes": 0,
            "fecha": datetime.utcnow(),
            "entity_type": "curso",
            "entity_id": str(curso_ids[1])
        }
    ]

    comentarios_clase = [
        {
            "title": "Gran explicación",
            "id_user": str(selected_users[2]),
            "content": "La lección sobre rutas en Flask fue muy clara.",
            "likes": 8,
            "dislikes": 0,
            "fecha": datetime.utcnow(),
            "entity_type": "clase",
            "entity_id": str(unidad_ids["Desarrollo Web con Flask"][0])  # ID de una clase específica
        }
    ]

    # Insertar comentarios en cursos
    for comentario in comentarios_curso:
        comment_id = mongo.db.comentarios.insert_one(comentario).inserted_id
        mongo.db.curso.update_one(
            {"_id": ObjectId(comentario["entity_id"])},
            {"$push": {"comentarios": comment_id}}
        )
        print(f"Comentario para curso '{comentario['title']}' insertado con ID: {comment_id}")

    # Insertar comentarios en clases
    for comentario in comentarios_clase:
        comment_id = mongo.db.comentarios.insert_one(comentario).inserted_id
        mongo.db.clase.update_one(
            {"_id": ObjectId(comentario["entity_id"])},
            {"$push": {"comentarios": comment_id}}
        )
        print(f"Comentario para clase '{comentario['title']}' insertado con ID: {comment_id}")

def populate_database():
    """Función principal para poblar la base de datos."""
    # Verifica si ya hay datos en la colección principal, por ejemplo, en `users`.
    if mongo.db.users.count_documents({}) > 0:
        print("La base de datos ya está poblada. No se realizará la población.")
        return

    # Población de datos
    user_ids = populate_users()
    curso_ids = populate_courses(user_ids)
    unidad_ids = populate_units(curso_ids)
    populate_classes(unidad_ids)
    populate_comments(user_ids, curso_ids, unidad_ids)

    print("Base de datos poblada correctamente.")


