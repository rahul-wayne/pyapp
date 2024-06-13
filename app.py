from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# MongoDB connection
#client = MongoClient('mongodb://172.17.0.1:27017/')
client = MongoClient('mongodb://mongodb-service:27017/')
db = client['microserviceDB']
collection = db['data']

@app.route('/')
def index():
    return render_template('add_data.html')

@app.route('/data', methods=['POST'])
def add_data():
    data = request.form
    result = collection.insert_one({'title': data['title'], 'content': data['content']})
    return redirect(url_for('view_data'))

@app.route('/data', methods=['GET'])
def view_data():
    try:
        data = list(collection.find())
        for item in data:
            item['_id'] = str(item['_id'])
        return render_template('view_data.html', data=data)
    except Exception as e:
        print(e)  # Print any error to the console
        return str(e)  # Optionally return the error as a response

@app.route('/delete/<id>', methods=['GET'])
def delete_data(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('view_data'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
