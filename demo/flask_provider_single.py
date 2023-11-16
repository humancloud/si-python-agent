#
# Copyright (c) 2019 Stackinsights to present
# All rights reserved
#from flask import Flask, jsonify
from flask import Flask, jsonify

from stackinsights import agent, config

config.init(agent_collector_backend_services='192.168.1.36:11800', agent_protocol='grpc',
            agent_name='great-app-provider-grpc',
            kafka_bootstrap_servers='192.168.1.36:9094',  # If you use kafka, set this
            agent_instance_name='instance-01',
            agent_experimental_fork_support=True,
            agent_logging_level='DEBUG',
            agent_log_reporter_active=True,
            agent_meter_reporter_active=True,
            agent_profile_active=True)


agent.start()

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def application():
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True, use_reloader=False)
