from config import app, api, db
from flask_restful import Resource
from models import User
from flask import make_response, request   
import jwt
import os



class Index(Resource):
    def get(self):
        return f""" howdy """

class Users(Resource):
    def get(self):
        users = [u.to_dict() for u in User.query.all() ]
        if not users:
            return make_response({"error":"no users found"}, 404)
        
        return make_response(users, 200)
    
    def post(self):
        data = request.get_json()
        useremail = data['email']
        checkuser = User.query.filter(User.email == useremail).first()

        if checkuser:
            return make_response({"error":"user with this email already exists"}, 400)

        if checkuser == None:
            try:
                newUser = User(
                    first=data['first'],
                    last=data['last'],
                    email=data['email']
                )

            except:
                return make_response({"error":"unable to create user"}, 400)

            try:
                tryPassword = data['password']
                newUser.password_hash = tryPassword

            except:
                return make_response({"error":"passwword unable to be set"}, 400)
            
            try:
                db.session.add(newUser)
                db.session.commit()

                token = jwt.encode({
                    'id': newUser.id, 
                    # 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
                    }, os.getenv('SECRET_KEY'))
                return make_response({'token': token.decode('UTF-8'), 'user': newUser.to_dict()}, 201)
            
            except:
                return make_response({"error":"unable to commit to database"}, 400)


class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_response({"error":"user not found"}, 404)
        
        return make_response(user.to_dict(), 200)
    
class Login(Resource):
    def post(self):
        print("reached the login post")
        username = request.get_json()['email']
        pw = request.get_json()['password']
        user = User.query.filter_by(email = username).first()
        checkuser = User.query.filter(User.email == username).first()

        if not checkuser:
            print("no user found")
            return make_response({"error":"username email not found"})
        
       
        if checkuser.authenticate(pw):
            token = jwt.encode({'id': checkuser.id},  os.getenv('SECRET_KEY'))
            return make_response({'token' : token, 'user' : checkuser.to_dict()}, 200)

        return make_response({"error":"Authentication failed"}, 400)

class FindPartnerById(Resource):
    def post(self):
        email = request.get_json()

        
        partner = User.query.filter_by(email = email).first()
        if partner is None:
            return make_response({"message": "no user found with that email"}, 404)
        
        return make_response(partner.to_dict(), 200)


api.add_resource(Index, '/' )
api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(FindPartnerById, '/findpartner')


if __name__ == '__main__':
    app.run(port=5555, host='0.0.0.0', debug=True)
