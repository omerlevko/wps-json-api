from flask import Flask, jsonify, request
from owslib.wps import WebProcessingService, ComplexDataInput
import json
from utils import parse_description, parse_outputs
from constants import Constants

wps = WebProcessingService(Constants.WPS_SERVER_URL, verbose=False, skip_caps=True)
app = Flask(__name__)


@app.route('/isAlive', methods=['GET'])
def is_alive():
    return 'im alive'


@app.route('/getCapabilities', methods=['GET'])
def get_capabilities():
    wps.getcapabilities()
    processes = wps.processes
    return jsonify([p.identifier for p in processes])


@app.route('/describeProcess/<process_identifier>', methods=['GET'])
def describe_process(process_identifier):
    metadata = wps.describeprocess(process_identifier)
    return jsonify(parse_description(metadata))


@app.route('/executeProcess/<process_name>', methods=['POST'])
def execute_process(process_name):
    data = json.loads(request.data)
    process_data = []
    if Constants.DATA_PROPERTY in data.keys():
        data_tuples = [(k, v) for k, v in data[Constants.DATA_PROPERTY].items()]
        process_data = process_data + data_tuples
    if Constants.GEO_DATA_PROPERTY in data.keys():
        geo_date_tuples = [(k, ComplexDataInput(v, Constants.GEOJSON_FORMAT))
                           for k, v in data[Constants.GEO_DATA_PROPERTY].items()]
        process_data = process_data + geo_date_tuples
    execution = wps.execute(process_name, process_data)
    outputs = execution.processOutputs
    return jsonify(parse_outputs(outputs))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
