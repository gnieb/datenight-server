from config import app, api, db
from flask_restful import Resource
from models import User
from flask import make_response




class Index(Resource):
    def get(self):
        return f""" howdy """
    

class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response({"error":"user not found"}, 404)
        
        return make_response(user.to_dict(), 200)


api.add_resource(Index, '/' )
api.add_resource(UserById, '/users/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
