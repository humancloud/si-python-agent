#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

from elasticsearch import Elasticsearch


if __name__ == '__main__':
    from flask import Flask, jsonify

    app = Flask(__name__)
    client = Elasticsearch('http://elasticsearch:9200/')
    index_name = 'test'

    def create_index():
        client.indices.create(index=index_name, ignore=400)

    def save_index():
        data = {'song': 'Despacito', 'artist': 'Luis Fonsi'}
        client.index(index=index_name, doc_type='test', id=1, body=data)

    def search():
        client.get(index=index_name, id=1)

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        create_index()
        save_index()
        search()
        return jsonify({'song': 'Despacito', 'artist': 'Luis Fonsi'})

    PORT = 9090
    app.run(host='0.0.0.0', port=PORT, debug=True)
