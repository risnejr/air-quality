from flask import Flask, Response
from flask_cors import CORS

import json
import grpcapi_pb2
import grpcapi_pb2_grpc
import dial_grpc
import csv
from collections import defaultdict


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


def read_ids(csv_file):
    node_ids = defaultdict(dict)

    with open(csv_file, 'r') as f:
        next(f)
        for row in csv.reader(f, skipinitialspace=True, delimiter=','):
            node_ids[row[0]].update({row[1]: row[2]})

    return node_ids


def sse_pack(d):
    buffer = ''
    for k in ['retry', 'id', 'event', 'data']:
        if k in d.keys():
            buffer += '{}: {}\n'.format(k, d[k])
    return buffer + '\n'


@app.route('/grpc/<asset>')
def grpc_generator(asset):
    channel = dial_grpc.dial()
    stub = grpcapi_pb2_grpc.IoTStub(channel)
    stream = stub.GetNodeDataStream(grpcapi_pb2.
                                    GetNodeDataStreamInput())

    node_ids = list(read_ids('node_ids.csv')[asset].values())

    def event_stream(event_id, channel):
        for data in stream:
            if any([data.node_id == node_id for node_id in node_ids]):
                if data.node_data.data_point.coordinate.y == 0:
                    node_data = data.node_data.question_answers[0]
                else:
                    node_data = data.node_data.data_point.coordinate.y
                msg = ({'event': 'delta',
                        'data': json.dumps({
                            'node_id': data.node_id,
                            'node_data': node_data
                            }),
                        'id': event_id})
                yield sse_pack(msg)
                event_id += 1
        channel.close()

    return Response(event_stream(0, channel), mimetype='text/event-stream')
