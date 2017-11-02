from flask import Flask
from flask import jsonify
from flask_cors import CORS

import salt.client

app = Flask(__name__)
CORS(app)

caller = salt.client.Caller()

id_to_service = {}

@app.route('/')
def get_stats():
    ret = {}

    stats_ret = caller.cmd('publish.runner','docker.stats')

    for host,host_data in stats_ret.items():
        ret[host] = {}
        ret[host]['stats'] = []
        for stat in host_data['stats']:
            container_id = stat['container']

            # If we already know the service name use it
            if container_id in id_to_service:
                container_name = id_to_service[container_id]
            # We need to lookup the service name
            else:
                host_ret = caller.cmd('publish.runner','docker.get_container_name',[container_id,host])
                # If we get a string, use it for the service name
                if host_ret:
                    container_name = host_ret
                    id_to_service[container_id] = host_ret
                # Else we use unknown for service name
                else:
                    container_name = 'Unknown'
            ret[host]['stats'].append({"name": container_name, "cpu_percent": stat['cpu_percent']})

    return jsonify(ret)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9999)
