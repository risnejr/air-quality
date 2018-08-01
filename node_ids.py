import dial_grpc
import grpcapi_pb2
import grpcapi_pb2_grpc
import argparse


def generate_dict(asset='', parent_id=''):
    response = stub.GetChildNodes(grpcapi_pb2.PrimitiveString(value=parent_id))
    try:
        nodes = response.ListFields()[0][1]
        for node in nodes:
            if node.type == 'asset':
                asset = node.label.lower()
                node_ids[asset] = {}
            else:
                node_ids[asset].update({node.label.lower(): node.id})
            generate_dict(asset, node.id)

    except:
        pass


def generate_csv():
    with open('node_ids.csv', 'w') as f:
        f.write('asset,inspection_point,node_id\n')
        for asset in node_ids:
            for inspection_point in node_ids[asset]:
                f.write('{},{},{}\n'.format(asset,
                                            inspection_point,
                                            node_ids[asset][inspection_point]))


channel = dial_grpc.dial()
stub = grpcapi_pb2_grpc.HierarchyStub(channel)

parser = argparse.ArgumentParser()
parser.add_argument('--id', help='node id from selected function location')
args = parser.parse_args()

node_ids = {}
generate_dict(parent_id=args.id)
generate_csv()

channel.close()
