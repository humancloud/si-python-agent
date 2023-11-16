#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#
import os

from flask import Flask
from stackinsights import agent, config
import requests

# Profiling only available in gRPC, meter only in kafka + grpc
config.init(agent_collector_backend_services='localhost:11800', agent_protocol='grpc',
            agent_name='great-app-consumer-grpc',
            kafka_bootstrap_servers='localhost:9094',  # If you use kafka, set this
            agent_instance_name='instance-01',
            agent_experimental_fork_support=True, agent_logging_level='DEBUG', agent_log_reporter_active=True,
            agent_meter_reporter_active=True,
            agent_profile_active=True)

agent.start()

parent_pid = os.getpid()
pid = os.fork()

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def application():
    res = requests.get('http://localhost:9999')
    return res.json()


if __name__ == '__main__':
    PORT = 9097 if pid == 0 else 9098  # 0 is child process
    app.run(host='0.0.0.0', port=PORT, debug=False)  # RELOADER IS ALSO FORKED
