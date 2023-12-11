from config import app, api, db
from flask_restful import Resource
from models import User
from flask import make_response, request   



class Index(Resource):
    def get(self):
        return f""" howdy """

class Users(Resource):
    def get(self):
        users = [u.to_dict() for u in User.query.find_all() ]
        if not users:
            return make_response({"error":"no users found"}, 404)
        
        return make_response(users, 200)
    
    def post(self):
        data = request.get_json()

        newUser = User(

        )
    

class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response({"error":"user not found"}, 404)
        
        return make_response(user.to_dict(), 200)


api.add_resource(Index, '/' )
api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
