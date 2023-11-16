#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time

from flask import Flask, jsonify
from pymongo import MongoClient

client = MongoClient('mongodb://mongo:27017/')
db = client['test-database']
collection = db['test-collection']


app = Flask(__name__)


@app.route('/insert_many', methods=['GET'])
def test_insert_many():
    time.sleep(0.5)
    new_posts = [{'song': 'Despacito'},
                 {'artist': 'Luis Fonsi'}]
    result = collection.insert_many(new_posts)
    return jsonify({'ok': result.acknowledged})


@app.route('/find_one', methods=['GET'])
def test_find_one():
    time.sleep(0.5)
    result = collection.find_one({'song': 'Despacito'})
    # have to get the result and use it. if not lint will report error
    print(result)
    return jsonify({'song': 'Despacito'})


@app.route('/delete_one', methods=['GET'])
def test_delete_one():
    time.sleep(0.5)
    result = collection.delete_one({'song': 'Despacito'})
    return jsonify({'ok': result.acknowledged})


if __name__ == '__main__':
    PORT = 9091
    app.run(host='0.0.0.0', port=PORT, debug=True)
