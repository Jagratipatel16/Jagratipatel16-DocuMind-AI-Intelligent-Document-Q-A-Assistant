from database.auth import hash_password
from database.auth import verify_password


password = "123456"

hashed = hash_password(password)

print("Original Password :", password)
print("Hashed Password   :", hashed)

print()

print("Correct Password :", verify_password("123456", hashed))

print("Wrong Password   :", verify_password("abcdef", hashed))