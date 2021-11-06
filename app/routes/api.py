from types import MethodDescriptorType
from flask import Blueprint, json, request, jsonify, session
from sqlalchemy.sql.expression import false
from app.models import User
from app.db import get_db
import sys
bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST']) #create
def signup():
    data = request.get_json()
    db = get_db()
    try:
        #create user
        newUser = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
        )
        #save to db
        db.add(newUser)
        db.commit()
    #handle error
    except:
        print(sys.exc_info()[0])
        #rollback
        db.rollback()
        return jsonify(message='Signup failed'), 500
    session.clear()
    session['user_id'] = newUser.id
    session['loggedIn'] = True
    return jsonify(id=newUser.id)

@bp.route('/users/logout', methods=['POST']) #logout
def logout():
    #remove session
    session.clear()
    return '', 204

@bp.route('/users/login', methods=['POST']) #login
def login():
  data = request.get_json()
  db = get_db()
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])
    return jsonify(message='Incorrect Credentials'), 400
  if user.verify_password(data['password']) == False:
      return jsonify(message = 'Incorrect Credentials'), 400
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True
  return jsonify(id=user.id)
