from flask import Blueprint
from services.classes_service import get_class_by_id

classes = Blueprint('classes', __name__)

#detalle de una clase por su ID
@classes.route('/<id>', methods=['GET'])
def get_class(id):
    return get_class_by_id(id)
