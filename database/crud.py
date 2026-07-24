from sqlalchemy.orm import Session

from database.models import User

from database.auth import hash_password
from database.auth import verify_password


# -----------------------------------
# Register New User
# -----------------------------------

def create_user(db: Session, name: str, email: str, password: str):

    existing_user = db.query(User).filter(
        User.email == email
    ).first()

    if existing_user:
        return None

    new_user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -----------------------------------
# Get User by Email
# -----------------------------------

def get_user_by_email(db: Session, email: str):

    return db.query(User).filter(
        User.email == email
    ).first()


# -----------------------------------
# Login User
# -----------------------------------

def login_user(db, email: str, password: str):

    user = get_user_by_email(db, email)

    if user is None:
        return None

    if verify_password(password, user.password):
        return user

    return None