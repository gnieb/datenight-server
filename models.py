from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
import re
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

# FoodieSpot
# activity


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String, nullable=False)
    last = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    _password_hash = db.Column(db.String)

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed')
    
    @password_hash.setter
    def password_hash(self, pw):
        if len(pw) < 8:
            raise ValueError("password must have more than 7 characters")
        password_hash = bcrypt.generate_password_hash(pw.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, pw):
        return bcrypt.check_password_hash(
            self._password_hash,
            pw.encode('utf-8')
        )
    
    @validates('email')
    def validate_email(self, key, address):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+');
        if re.fullmatch(regex, address):
            return address
        raise ValueError("Not a valid email address")



class FoodJoint(db.Model, SerializerMixin):
    __tablename__ = 'foodjoints'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)



class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

