#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#


if __name__ == '__main__':
    from flask import Flask, jsonify
    app = Flask(__name__)
    import pika
    parameters = (pika.URLParameters('amqp://admin:admin@rabbitmq-server:5672/%2F'))

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare('test')
        channel.exchange_declare('test')
        channel.queue_bind(exchange='test', queue='test', routing_key='test')
        channel.basic_publish(
            exchange='test', routing_key='test',
            properties=pika.BasicProperties(headers={'key': 'value'}),
            body=b'Test message.')
        connection.close()

        return jsonify({'song': 'Despacito', 'artist': 'Luis Fonsi'})

    PORT = 9090
    app.run(host='0.0.0.0', port=PORT, debug=True)
