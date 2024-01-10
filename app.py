from config import app, api, db, mail
from flask_restful import Resource
from models import User
from flask import make_response, request, render_template  
import jwt
import os
from flask_mail import Mail, Message


class Index(Resource):
    def get(self):
        return f""" howdy """
    
@app.route('/home')
def get():
    return render_template("partnerEmail.html")

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
                return make_response({"error":"unable to commit new user to database"}, 400)


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
        print(partner.email)
        
        return make_response(partner.to_dict(), 200)
    # this will eventually need to a be a POST method because I need the following info:
    # the button needs to do the final linking:
    # I think the button will need to run a script that just conducts a PATCH for the existing user:
    # need:
    # BOTH user emails
    # BOTH suer ID's 

@app.route('/test/<string:email>', methods=['PATCH'])
def link(email):
    if request.method == 'PATCH':
        user = User.query.filter_by(email= email).first()

        if not user:
            return make_response({"error":"No user found"}, 404)

        try:
            data = request.get_json()
            for key in data.keys():
                setattr(user, key, data[key])   
        except:
            return make_response({"error":"patch unsuccessful"}, 400)
        try:
            db.session.add(user)
            db.session.commit()
            return make_response(user.to_dict(), 200)

        except:
            return make_response({"error":"db constraint validation error"}, 422)
            





    
@app.route('/send/<string:email>')
def email(email):
    mail_message = Message(
    'Your Partner Wants to Connect on the Date Night App!', 
    sender =   'graycee.nieb@gmail.com', 
    recipients = [email])
    mail_message.body = f'''
    Would you like to connect to your partner on Date Night?
    '''
    mail_message.html = render_template('partnerEmail.html')
    mail.send(mail_message)
    print("Mail was sent!")
    return make_response({"msg":"Mail has sent"}, 200)


api.add_resource(Index, '/' )
api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<int:id>')
api.add_resource(Login, '/login')
api.add_resource(FindPartnerById, '/findpartner')


if __name__ == '__main__':
    app.run(port=5555, host='0.0.0.0', debug=True)
