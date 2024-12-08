from config.dynamodb import dynamodb
from botocore.exceptions import ClientError
from flask import jsonify
from config.mongodb import mongo
from bson import ObjectId


def add_user(data):
    table = dynamodb.Table('Users')
    try:
        table.put_item(Item={
            'username': data['username'],
            'password': data['password']
        })
        return {'message': 'Usuario agregado con éxito'}
    except ClientError as e:
        raise Exception(f"Error al agregar usuario: {str(e)}")

def get_user(username):
    table = dynamodb.Table('Users')
    try:
        response = table.get_item(Key={'username': username})
        if 'Item' in response:
            return response['Item']
        else:
            return {'message': 'Usuario no encontrado'}
    except ClientError as e:
        raise Exception(f"Error al obtener usuario: {str(e)}")


def enroll_user_in_course(username, course_id):
    table = dynamodb.Table('UserCourses')
    try:
        course_id = str(course_id)
        response = table.update_item(
            Key={'username': username},
            UpdateExpression="ADD courses :course_id",
            ExpressionAttributeValues={
                ':course_id': {course_id}
            },
            ReturnValues="UPDATED_NEW"
        )
        return jsonify({"message": f"Usuario {username} inscrito en el curso {course_id}"}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 500


def login(data):
    table = dynamodb.Table('Users')
    try:
        response = table.get_item(Key={'username': data['username']})
        if 'Item' not in response:
            return {'error': 'Usuario no encontrado'}, 404
        if response['Item']['password'] == data['password']:
            return {'message': 'Inicio de sesión exitoso'}, 200
        else:
            return {'error': 'Contraseña incorrecta'}, 401
    except ClientError as e:
        raise Exception(f"Error al intentar hacer login: {str(e)}")
