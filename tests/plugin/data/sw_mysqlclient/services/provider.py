#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import time

if __name__ == '__main__':
    from flask import Flask, jsonify
    import MySQLdb

    app = Flask(__name__)

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        time.sleep(0.5)
        connection = MySQLdb.connect(host='mysql', user='root', passwd='root', db='mysql', charset='utf8mb4')
        with connection.cursor() as cursor:
            sql = 'select * from user where user = %s'
            cursor.execute(sql, ('root',))

        connection.close()

        return jsonify({'song': 'Despacito', 'artist': 'Luis Fonsi'})

    PORT = 9091
    app.run(host='0.0.0.0', port=PORT, debug=True)
