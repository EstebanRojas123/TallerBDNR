from flask import Blueprint
from services.classes_service import get_class_by_id
from services import comments_service

classes = Blueprint('classes', __name__)

#detalle de una clase por su ID
@classes.route('/<id>', methods=['GET'])
def get_class(id):
    return get_class_by_id(id)

# En class_routes.py
@classes.route('/<class_id>/comment', methods=['POST'])
def create_comment(class_id):
    return comments_service.create_comment_service(entity_type="clase", entity_id=class_id)

