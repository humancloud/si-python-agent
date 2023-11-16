#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

import happybase


if __name__ == '__main__':
    from flask import Flask, jsonify

    app = Flask(__name__)
    connection = happybase.Connection('hbase', port=9090)
    connection.open()
    row = b'row_key'
    info = {b'INFO:data': b'value'}
    table_name = 'test'

    def create_table():
        families = {'INFO': {}}
        connection.create_table(table_name, families)

    def save_table():
        table = connection.table(table_name)
        table.put(row, info)

    def get_row():
        table = connection.table(table_name)
        table.row(row)

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        create_table()
        save_table()
        get_row()
        return jsonify({'INFO:data': 'value'})

    PORT = 9090
    app.run(host='0.0.0.0', port=PORT, debug=True)
