import string
from sqlalchemy.orm import Session
from model.user import User


def get_user_by_id(db: Session, id: string) -> User:
    return db.query(User).filter(User.id == id).one()


def get_user_by_email(db: Session, email: string) -> User:
    return db.query(User).filter(User.email == email).one()


def save_user(db, user: User):
    db.add(user)
    db.commit()
