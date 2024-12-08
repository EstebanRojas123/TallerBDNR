from flask import Blueprint, request, jsonify
from services.dynamodb_service import add_user, get_user, enroll_user_in_course, login
from config.dynamodb import dynamodb
from botocore.exceptions import ClientError

dynamodb_bp = Blueprint('dynamodb', __name__)

@dynamodb_bp.route('/add_user', methods=['POST'])
def add_user_route():
    data = request.json
    try:
        result = add_user(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dynamodb_bp.route('/get_user/<username>', methods=['GET'])
def get_user_route(username):
    try:
        result = get_user(username)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dynamodb_bp.route('/enroll_user', methods=['POST'])
def enroll_user():
    data = request.get_json()
    username = data['username']
    course_id = data['course_id']
    enroll_response = enroll_user_in_course(username, course_id)
    return enroll_response

@dynamodb_bp.route('/get_user_courses', methods=['GET'])
def get_user_courses():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400
    try:
        table = dynamodb.Table('UserCourses')
        response = table.get_item(Key={'username': username})
        if 'Item' not in response:
            return jsonify({"error": f"No courses found for user {username}"}), 404
        user_courses = response['Item'].get('courses', [])
        if isinstance(user_courses, set):
            user_courses = list(user_courses)
        return jsonify({"username": username, "courses": user_courses}), 200
    except ClientError as e:
        return jsonify({"error": str(e)}), 500

@dynamodb_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username y password son requeridos'}), 400
    result, status_code = login(data)
    return jsonify(result), status_code
