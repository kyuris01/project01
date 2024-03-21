from flask import Blueprint

routing_object = Blueprint('route', __name__)

@routing_object.route('route1')
def route1():
    return "Test Route1"