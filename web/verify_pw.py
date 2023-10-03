import user_exists as u
import bcrypt
from pymongo import MongoClient


#connect to mongodb 
client = MongoClient("mongodb://db:27017")
db = client.myDB
users = db["users"]


def verify_pw(username, password):
    if not u.user_exists(username):
        return False
    hashed_pw = users.find({"username": username})[0]["password"]
    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else: 
        False