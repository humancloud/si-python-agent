#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#

"""
sw-python -d run -p uwsgi --die-on-term \
    --http 0.0.0.0:9090 \
    --http-manage-expect \
    --workers 2 \
    --worker-reload-mercy 30 \
    --enable-threads \
    --threads 1 \
    --manage-script-name \
    --mount /=flask_consumer_prefork:app
"""
from flask import Flask
import logging

app = Flask(__name__)


# This is wrong!! Do not do this with prefork server, fork support (os.fork) do not work with uWSGI!
# from stackinsights import agent, config
#
# config.init(agent_collector_backend_services='127.0.0.1:11800', agent_name='your awesome service',
# agent_logging_level ='DEBUG', agent_experimental_fork_support=True)
#
# agent.start()


@app.route('/cat', methods=['POST', 'GET'])
def artist():
    try:
        logging.critical('fun cat got a request')
        return {'Cat Fun Fact': 'Fact is cat, cat is fat'}
    except Exception as e:  # noqa
        return {'message': str(e)}


if __name__ == '__main__':
    # noinspection PyTypeChecker
    # app.run(host='0.0.0.0', port=9090)
    ...
