from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from base64 import b64encode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    hashed_password = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(25), unique=True, nullable=False)
    location = db.Column(db.String (50), nullable=False)

    # def __repr__(self):
    #     return '<User %r>' % self.username

    
    def __init__(self,**body):
        #se crea la función constructora para las instancias
        self.full_name = body ['full_name']
        self.salt = b64encode(os.urandom(4)).decode('utf-8')
        self.hashed_password = self.set_password(body['password'])
        self.email = body ['email']
        self.phone = body ['phone']
        self.location = body ['location']
       
        #función para guardar la contraseña
    def set_password(self, password):
        return generate_password_hash(
            f"{password}{self.salt}"
    ) 

        #función para chequear la contraseña
    def check_password(self, password):
        return check_password_hash(
            self.hashed_password,
            f"{password}{self.salt}"
        )

    @classmethod
    def create (cls,**kwargs):
        new_user=cls(kwargs)
        db.session.add(new_user)
        db.session.commit()
        return new_user    

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
        }    

    