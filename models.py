from config import db
from sqlalchemy_serializer import SerializerMixin
import re

# FoodieSpot
# activity

class FoodJoint(db.Model, SerializerMixin):
    __tablename__ = 'foodjoints'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable=False)
    


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

