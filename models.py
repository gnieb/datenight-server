from config import db, bcrypt
from sqlalchemy_serializer import SerializerMixin
import re
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

# FoodieSpot
# activity


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-activities.user', '-partner', '-partner_')

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String, nullable=False)
    last = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String)
    activities = db.relationship('Activity', backref='user' )

    # New field for one-to-one relationship with User
    partner_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), unique=True)
    # Add a back reference for the partner relationship
    partner = db.relationship('User', remote_side=[id], uselist=False, backref='partner_')


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
    # this should return a boolean
    
    @validates('email')
    def validate_email(self, key, address):
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+');
        if re.fullmatch(regex, address):
            return address
        raise ValueError("Invalid email address format. Please check the email format and try again.")
    
    @validates('partner_id')
    def validate_partner_id(self, key, partner_id):
        if partner_id is not None and self.partner is not None:
            raise ValueError("User can only have one partner")
        return partner_id



class FoodJoint(db.Model, SerializerMixin):
    __tablename__ = 'foodjoints'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False) 
    # location - full string? 

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String)
    season = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    @validates('category')
    def validate_category(self, key, cat):
        valid_categories = [ 'spicy', 'silly', 'lazy', 'fun' ]
        if cat in valid_categories:
            return cat
        raise ValueError(f"Invalid category. Please choose one of the following: {', '.join(valid_categories)}")
        
    @validates('season')
    def validate_season(self, key, season):
        if season in ['fall', 'winter', 'spring', 'summer']:
            return season
        raise ValueError("Season must be one of the following: FALL, WINTER, SPRING, SUMMER")


class Conversation(db.Model, SerializerMixin):
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    


class Message (db.Model, SerializerMixin):

    id = db.Column(db.Integer, primary_key=True)
    text= db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
