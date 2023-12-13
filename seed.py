from config import db
from models import User, Activity, FoodJoint

def seedDatabase():
    print("deleting data")
    db.drop_all()

    db.create_all()

    u1 = User(first='Grace', last='Nieboer', email='grace@gmail.com')
    

    


if __name__ == '__main__':
    seedDatabase()