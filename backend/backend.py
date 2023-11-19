from flask import Flask
from flask import Blueprint, request, jsonify
from Learning import predict, load_model

app = Flask(__name__)

model = load_model()

@app.route('/api/detect', methods=['POST'])
def api_detect():
    data = request.get_json()
    # print("Hello World")

    strings = data['strings']
    result = predict(strings, model)

    
    return result

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port='5000')
