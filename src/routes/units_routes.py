from flask import Blueprint, jsonify
from services.units_service import get_units_by_ids, get_classes_by_unit_id

units = Blueprint('units', __name__)

#obtener una unidad específica
@units.route('/<id>', methods=['GET'])
def get_unit(id):
    return jsonify(get_units_by_ids([id])), 200

# obtener las clases de una unidad específica
@units.route('/<id>/classes', methods=['GET'])
def get_classes_by_unit(id):
    return get_classes_by_unit_id(id)
