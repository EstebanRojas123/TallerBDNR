from flask import Blueprint,request,jsonify
from services import courses_service, comments_service

courses = Blueprint('courses', __name__)

@courses.route('/', methods=['POST'])
def create_course():
    return courses_service.create_course_service()


@courses.route('/', methods=['GET'])
def get_all_courses():
    return courses_service.get_all_courses_service()


@courses.route('/<id>', methods=['GET'])
def get_course(id):
    return courses_service.get_course_by_id(id)


@courses.route('/<course_id>/register', methods=['POST'])
def register_user(course_id):
    data = request.get_json()
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Se requiere el ID del usuario"}), 400

    return courses_service.register_user_in_course(course_id, user_id)


@courses.route('/<course_id>/rating', methods=['POST'])
def add_course_rating(course_id):
    return courses_service.add_course_rating_service(course_id)



@courses.route('/<course_id>/comment', methods=['POST'])
def add_course_comment(course_id):
    return courses_service.add_course_comment_service(course_id)
