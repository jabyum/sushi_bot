from database.models import User, Admin
from database import get_db
from datetime import datetime

def register_user(user_id, user_name, phone_number):
    db = next(get_db())
    new_user = User(tg_id=user_id, user_name=user_name,
                        phone_number=phone_number, reg_date=datetime.now())
    db.add(new_user)
    db.commit()

def check_user_db(user_id):
    db = next(get_db())
    checker = db.query(User).filter_by(tg_id=user_id).first()
    if checker:
        return True
    return False
def change_language(user_id, new_language):
    db = next(get_db())
    user = db.query(User).filter_by(user_id=user_id).first()
    user.language = new_language
    db.commit()
def change_user_info(user_id, column, new_info):
    db = next(get_db())
    all_info = db.query(User).filter_by(user_id=user_id).first()
    if column == "user_name":
        all_info.user_name = new_info
    elif column == "phone_number":
        all_info.phone_number = new_info
    db.commit()
def get_user_info(user_id):
    db = next(get_db())
    checker = db.query(User).filter_by(tg_id=user_id).first()
    if checker:
        return [checker.phone_number, checker.language]

def register_admin(admin_id, admin_name):
    db = next(get_db())
    try:
        add_admin = Admin(admin_tg_id=admin_id, admin_name=admin_name)
        db.add(add_admin)
        db.commit()
    except:
        pass
def check_admin(user_id):
    db = next(get_db())
    checker = db.query(Admin).filter_by(admin_tg_id=user_id).first()
    if checker:
        return True
    return False
