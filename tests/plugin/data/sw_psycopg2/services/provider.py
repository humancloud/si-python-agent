#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time


if __name__ == '__main__':
    from flask import Flask, jsonify
    import psycopg2

    app = Flask(__name__)

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        time.sleep(0.5)
        connection = psycopg2.connect(host='postgres', user='root', password='root', dbname='admin')
        with connection.cursor() as cursor:
            sql = 'select * from user where user = %s'
            cursor.execute(sql, ('root',))

        connection.close()

        return jsonify({'song': 'Despacito', 'artist': 'Luis Fonsi'})

    PORT = 9091
    app.run(host='0.0.0.0', port=PORT, debug=True)
