from flask import Blueprint, request, render_template, redirect, url_for

routing_object = Blueprint('route', __name__) #블루프린트객체이름 = Blueprint(블루프린트이름, __name__)


@routing_object.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html') 
    else:
