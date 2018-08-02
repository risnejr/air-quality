import dial_grpc
import grpcapi_pb2
import grpcapi_pb2_grpc
import argparse
import json


def generate_json(node_ids={}, fl='', asset='', parent_id=''):
    response = stub.GetChildNodes(grpcapi_pb2.PrimitiveString(value=parent_id))

    try:
        nodes = response.ListFields()[0][1]
        for node in nodes:
            if node.type == 'functional_location':
                fl = node.label.lower().replace(' ', '_')
                node_ids[fl] = {}
            elif node.type == 'asset':
                asset = node.label.lower().replace(' ', '_')
                node_ids[fl].update({asset: {}})
            else:
                ip = node.label.lower().replace(' ', '_')
                node_ids[fl][asset].update({ip: node.id})
            generate_json(node_ids, fl, asset, node.id)

        return node_ids
    except:
        pass


parser = argparse.ArgumentParser()
parser.add_argument('--id', help='node id from selected function location')
args = parser.parse_args()

channel = dial_grpc.dial()
stub = grpcapi_pb2_grpc.HierarchyStub(channel)
root_id = stub.GetParentNode(grpcapi_pb2.PrimitiveString(value=args.id)).id

data = generate_json(parent_id=root_id)

with open('config.json', 'w') as f:
    json.dump(data, f, indent=2)

channel.close()
