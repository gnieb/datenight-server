from config import db, app
from models import User, Activity, FoodJoint

def seedDatabase():
    print("deleting data")
    # db.drop_all()

    # db.create_all()

    # DONE u1 = User(first='Grace', last='Nieboer', email='grace@gmail.com')

    # a1 = Activity(name='ice skating', category='fun', season='winter', user_id=1 )

    db.session.add(a1)
    db.session.commit()

    print("seeding complete!")



if __name__ == '__main__':
    with app.app_context():
        seedDatabase()