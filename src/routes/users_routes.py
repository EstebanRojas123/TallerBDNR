from flask import Blueprint
from services import user_services

users= Blueprint('users_', __name__)

@users.route('/',methods=['POST'])
def create_user():
    return user_services.create_user_service()

