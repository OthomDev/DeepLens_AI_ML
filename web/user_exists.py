from pymongo import MongoClient


#connect to mongodb 
client = MongoClient("mongodb://db:27017")
db = client.myDB
users = db["users"]





def user_exists(username):
    user = users.find_one({"username": username})
    #if users.count_documents({"username": username}) == 0:
    if user == None:
        return False
    return True