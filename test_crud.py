from database.database import SessionLocal

from database.crud import create_user
from database.crud import get_user_by_email


db = SessionLocal()

user = create_user(
    db,
    name="Jagrati",
    email="jagrati@gmail.com",
    password="123456"
)

if user:
    print("User Created Successfully")
else:
    print("User Already Exists")

print()

found = get_user_by_email(
    db,
    "jagrati@gmail.com"
)

print(found.name)
print(found.email)

db.close()