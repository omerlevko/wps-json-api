from flask import Flask, jsonify, request
from owslib.wps import WebProcessingService, ComplexDataInput
import json

wps = WebProcessingService('http://localhost:5000/wps', verbose=False, skip_caps=True)
app = Flask(__name__)


@app.route('/isAlive',methods=['GET'])
def is_alive():
    return 'im alive'


@app.route('/getCapabilities',methods=['GET'])
def get_capabilities():
    wps.getcapabilities()
    processes = wps.processes
    return jsonify([p.identifier for p in processes])


@app.route('/describeProcess/<process_identifier>',methods=['GET'])
def describe_process(process_identifier):
    metadata = wps.describeprocess(process_identifier)
    return jsonify(parse_description(metadata))


@app.route('/executeProcess/<process_name>', methods=['POST'])
def execute_process(process_name):
    data = json.loads(request.data)
    data_tuples = [(k, v) for k, v in data["data"].items()]
    # geo_date_tuples = [(k, ComplexDataInput(v,"application/vnd.geo+json"))
    #                    for k, v in data["geo_data"].items()]
    execution = wps.execute(process_name, data_tuples)
    outputs = execution.processOutputs
    return jsonify([out.data[0] for out in outputs])

def parse_description(description):
    delattr(description,"_root")
    description_json = json.dumps(description, default=lambda o: o.__dict__)
    return json.loads(description_json)


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)
