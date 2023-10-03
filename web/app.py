from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

from PIL import Image
from io import BytesIO


from PIL import Image
from tensorflow.keras.applications import InceptionV3, imagenet_utils
from tensorflow.keras.applications.inception_v3 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array


import user_exists as u
import verify_credentiels as vc
import verify_pw as vp
import generate_return_dictionary as g





app = Flask(__name__)
api = Api(app)




#Load the pre trained model:
pretrained_model = InceptionV3(weights="imagenet")



#connect to mongodb 
client = MongoClient("mongodb://db:27017")
db = client.myDB
users = db["users"]



class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if u.user_exists(username):
            retJson={
                "Status Code": 301,
                "msg": "The username provided is already in use. Kindly select an alternative username to proceed with the registration."
            }
            return jsonify(retJson)
        
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({"username": username, "password": hashed_pw, "Tokens": 6})

        retJson={
            "Status Code": 200,
            "msg": "You've successfully signed up to the API"
        }

        return jsonify(retJson)

















class Classify(Resource):
    def post(self):
        dataPosted = request.get_json()
        username = dataPosted["username"]
        password = dataPosted["password"]
        url = dataPosted["url"]

        # Verify the credentiels:

        retJson, error = vc.verify_credentiels(username, password)

        if error:
            return jsonify(retJson)
        
        # Check if the User has enough Tokens:

        tokens = users.find({"username": username})[0]["Tokens"]

        if tokens <= 0 : return jsonify(g.generate_return_dictionary(303, "Not enough Tokens"))

        # Classify the Image:

        if not url:
            return jsonify(({"error": "No url provided"}), 400)
        
        # return classification response:

        #Load image from url:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))

        # pre process the image:
        img = img.resize((299,299))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)


        # Make the predection:
        predection = pretrained_model.predict(img_array)
        actual_prediction = imagenet_utils.decode_predictions(predection, top=5) # 5 probabilities

        # Return the results
        retJson = {}

        for pred in actual_prediction[0]:
            retJson[pred[1]] = float(pred[2]*100)

        users.update_one({"username": username}, {"$set": {"Tokens": tokens - 1}})

        return jsonify(retJson)



class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        admin_pass = postedData["admin_pw"]
        amount = postedData["amount"]

        if not u.user_exists(username):
            return jsonify(g.generate_return_dictionary(301, "Invalid Username"))
        
        correct_pw = 'abc123'

        if not admin_pass == correct_pw:
            return jsonify(g.generate_return_dictionary(302, "Invalid Password"))
        
        # Update the token respond

        users.update_one({"username": username}, { "$set": { "Tokens": amount}})

        return jsonify(g.generate_return_dictionary(200, "Refilled !"))
    





















api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')



if __name__=='__main__':
    app.run(host='0.0.0.0')

