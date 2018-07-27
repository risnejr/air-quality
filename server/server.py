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
    for k in ['retry', 'id', 'event', 'data']:
        if k in d.keys():
            buffer += '{}: {}\n'.format(k, d[k])
    return buffer + '\n'


@app.route('/grpc')
def grpc_generator():
    # with dial_grpc.dial() as channel:
    channel = dial_grpc.dial()
    stub = grpcapi_pb2_grpc.IoTStub(channel)
    stream = stub.GetNodeDataStream(grpcapi_pb2.
                                    GetNodeDataStreamInput())

    def event_stream(event_id, channel):
        for data in stream:
            msg = ({'event': 'delta',
                    'data': json.dumps({
                        'node_id': data.node_id,
                        'node_data': data.node_data.data_point.coordinate.y
                        }),
                    'id': event_id})
            yield sse_pack(msg)
            event_id += 1
        channel.close()

    return Response(event_stream(0, channel), mimetype='text/event-stream')
