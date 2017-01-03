from flask import Flask, request
from flasgger import Swagger
from nameko.standalone.rpc import ClusterRpcProxy
from flasgger.utils import swag_from
import logging, subprocess, signal, os
app = Flask(__name__)
Swagger(app)
CONFIG = {'AMQP_URI': "amqp://guest:guest@localhost"}


@app.route('/send', methods=['POST'])
@swag_from('docs/send.yml')
def send():
    logger = app.logger
    process = subprocess.Popen('./startservice.sh', shell=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

    try:
        type = request.json.get('type')
        body = request.json.get('body')
        address = request.json.get('address')
        #logger.info('Get message: %s,%s,%s' % (type,body,address))
    except Exception, e:
        return 'Bad Request', 400

    with ClusterRpcProxy(CONFIG) as rpc:
        # asynchronously spawning and email notification
        rpc.yowsup.send(type,body,address)

    os.killpg(os.getpgid(process.pid), signal.SIGTERM)

    msg = "OK"
    return msg, 200

app.run(host='0.0.0.0', port=5000, debug=True)
