from flask import Flask
from flask import Blueprint, request, jsonify
from Learning import predict, load_model, label_map

app = Flask(__name__)

model = load_model()

@app.route('/api/detect', methods=['POST'])
def api_detect():
    data = request.get_json()
    # print("Hello World")
