from database.models import User, Admin
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
def register_user(user_id, user_name, phone_number, language):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    new_user = User(tg_id=user_id, user_name=user_name,
                        phone_number=phone_number, language=language, reg_date=datetime.now())
    db.add(new_user)
    db.commit()

def check_user_db(user_id):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    checker = db.query(User).filter_by(tg_id=user_id).first()
    if checker:
        return True
    return False
def get_all_users_id():
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    all_ids = db.query(User).all()
    if all_ids:
        return [i.tg_id for i in all_ids]
    return []

def check_language_db(user_id):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    checker = db.query(User).filter_by(tg_id=user_id).first()
    return checker.language
def change_language(user_id, new_language):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    try:
        user = db.query(User).filter_by(tg_id=user_id).first()
        user.language = new_language
        db.commit()
    except:
        pass
def change_user_info(user_id, column, new_info):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    all_info = db.query(User).filter_by(user_id=user_id).first()
    if column == "user_name":
        all_info.user_name = new_info
    elif column == "phone_number":
        all_info.phone_number = new_info
    db.commit()
def get_user_info(user_id):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    checker = db.query(User).filter_by(tg_id=user_id).first()
    if checker:
        return [checker.phone_number, checker.language]

def register_admin(admin_id, admin_name):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    try:
        add_admin = Admin(admin_tg_id=admin_id, admin_name=admin_name)
        db.add(add_admin)
        db.commit()
    except:
        pass
def check_admin(user_id):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    checker = db.query(Admin).filter_by(admin_tg_id=user_id).first()
    if checker:
        return True
    return False
def delete_admin_db(admin_id):
    engine = create_engine('sqlite:///data.db', echo=False, connect_args={'check_same_thread': False})
    db = Session(bind=engine)
    checker = db.query(Admin).filter_by(admin_tg_id=admin_id).first()
    db.delete(checker)
    db.commit()