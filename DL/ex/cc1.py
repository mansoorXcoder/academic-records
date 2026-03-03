from flask import Flask, jsonify, request
app = Flask(__name__)
data = [{
 'id': 1,
 'name': 'Sample Item 1'
}, {
 'id': 2,
 'name': 'Sample Item 2'
}]
@app.route('/', methods=['GET'])
def get_data():
 return jsonify(data)
if __name__ == '__main__':
 app.run(debug=True)
