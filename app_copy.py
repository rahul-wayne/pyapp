from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

# MongoDB connection
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['microserviceDB']
collection = db['data']

# Add data to MongoDB
@app.route('/data', methods=['POST'])
def add_data():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'_id': str(result.inserted_id)}), 201

# View all data from MongoDB
@app.route('/data', methods=['GET'])
def view_data():
    data = list(collection.find())
    for item in data:
        item['_id'] = str(item['_id'])
    return jsonify(data)

# Delete data from MongoDB
@app.route('/data/<id>', methods=['DELETE'])
def delete_data(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    if result.deleted_count:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': 'data not found'}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
