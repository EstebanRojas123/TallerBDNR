from flask import Blueprint
from services import courses_service 

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