#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

if __name__ == '__main__':
    topic = 'stackinsights'
    server_list = ['kafka-server:9092']
    group_id = 'stackinsights'
    client_id = '0'

    from kafka import KafkaConsumer
    from kafka import TopicPartition
    consumer = KafkaConsumer(group_id=group_id,
                             client_id=client_id,
                             bootstrap_servers=server_list)
    partition = TopicPartition(topic, int(client_id))
    consumer.assign([partition])
    for msg in consumer:
        print(msg)
