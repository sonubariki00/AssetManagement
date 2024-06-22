import json

import requests
from flask import Flask, request, jsonify

test = Flask(__name__)
p="p"
response = requests.get(f"http://localhost:5000/")
@test.route("/",methods=["GET"])
def printsonu():
    print("HII Sonu HOw R U")
    return "Hello Domicile"


if __name__=="main":
    test.run(debug=True)