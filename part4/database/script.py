from bcrypt import hashpw, gensalt
password = "admin1234"
hashed_password = hashpw(password.encode(), gensalt()).decode()
print(hashed_password)
