"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_current_user, get_jwt_identity
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['JWT_SECRET_KEY'] = 'super-secret'
#aquí cambiamos a super-secret
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
jwt = JWTManager(app) #se agrega para evitar este error 'You must initialize a JWTManager with this flask application before using this method
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

#para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def handle_user():
    users = User.query.all()
    response_body = []
    for user in users:
        response_body.append(user.serialize())
    return jsonify(response_body), 200

#para crear un usuario
@app.route('/users', methods=['POST'])
def add_new_professional():
    body = request.get_json()
    print (body)
    new_user = User(
        full_name = body ["full_name"],
        password = body ["password"],
        email = body ["email"],
        phone = body ["phone"],
        location = body ["location"],
       
    )
    db.session.add(new_user)
    try:
        db.session.commit()
        print (new_user.serialize())
        response = {'jwt': create_access_token (identity=new_user.email), "user": new_user.serialize()}
        return jsonify (response), 201
    except Exception as error:
        print (error.args)
        return jsonify ("NOT CREATE USER"), 500
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
