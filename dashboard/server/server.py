from flask import Flask, Response
from flask_cors import CORS

import json
import grpcapi_pb2
import grpcapi_pb2_grpc
import dial_grpc


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


def sse_pack(d):
    buffer = ''
    for k in ['id', 'event', 'data']:
        if k in d.keys():
            buffer += '{}: {}\n'.format(k, d[k])
    return buffer + '\n'


@app.route('/grpc/<func_loc>/<asset>')
def grpc_generator(func_loc, asset):
    channel = dial_grpc.dial()
    stub = grpcapi_pb2_grpc.IoTStub(channel)
    stream = stub.GetNodeDataStream(grpcapi_pb2.
                                    GetNodeDataStreamInput())

    with open('../../config.json', 'r') as f:
        node_ids = json.load(f)[func_loc][asset]

    def event_stream(event_id, channel):
        for data in stream:
            inspection_point = [ip for ip, node_id in node_ids.items() if data.node_id == node_id]
            if inspection_point:
                if data.node_data.data_point.coordinate.y == 0:
                    node_data = data.node_data.question_answers[0]
                else:
                    node_data = data.node_data.data_point.coordinate.y

                msg = ({'event': 'delta',
                        'data': json.dumps({
                            'node_id': data.node_id,
                            'node_data': node_data,
                            'inspection_point': inspection_point[0]
                            }),
                        'id': event_id})

                yield sse_pack(msg)
                event_id += 1
        channel.close()

    return Response(event_stream(0, channel), mimetype='text/event-stream')