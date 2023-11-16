#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

if __name__ == '__main__':
    import pika

    parameters = (pika.URLParameters('amqp://admin:admin@rabbitmq-server:5672/%2F'))

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    channel.queue_declare('test')
    channel.exchange_declare('test')
    channel.queue_bind(exchange='test', queue='test', routing_key='test')
    for method_frame, properties, body in channel.consume('test'):
        # Display the message parts and acknowledge the message
        print(method_frame, properties, body)
        channel.basic_ack(method_frame.delivery_tag)

        # Escape out of the loop after 10 messages
        if method_frame.delivery_tag == 10:
            break

    try:
        # Loop so we can communicate with RabbitMQ
        connection.ioloop.start()
    except KeyboardInterrupt:
        # Gracefully close the connection
        connection.close()
        # Loop until we're fully closed, will stop on its own
        connection.ioloop.start()
