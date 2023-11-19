from flask import Flask
from flask import Blueprint, request, jsonify
from Learning import predict, load_model, label_map
from flask_cors import CORS

from dotenv import load_dotenv
import os


# Load environment variables from .env
load_dotenv()
app = Flask(__name__)
CORS(app)

model = load_model()

@app.route('/api/detect', methods=['POST'])
def api_detect():
    data = request.get_json()
    # print("Hello World")

    print(data)
    strings = data['strings']
    print(strings)
    labels, prob = predict(strings, model)
    labels = [label_map[label] for label in labels]
    
    response = jsonify(labels=labels, prob=prob.tolist())
    
    return response


if __name__ == '__main__':
    app.run(debug=True, host=os.getenv('HOST'), port=os.getenv('PORT'))