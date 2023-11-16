#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#


if __name__ == '__main__':
    from flask import Flask, jsonify
    from kafka import KafkaProducer

    app = Flask(__name__)
    producer = KafkaProducer(bootstrap_servers=['kafka-server:9092'], api_version=(1, 0, 1))

    @app.route('/users', methods=['POST', 'GET'])
    def application():
        producer.send('stackinsights', b'some_message_bytes')

        return jsonify({'song': 'Despacito', 'artist': 'Luis Fonsi'})

    PORT = 9090
    app.run(host='0.0.0.0', port=PORT, debug=True)
