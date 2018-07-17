import sys
sys.path.append('./proto')

import grpc
import grpcapi_pb2
import grpcapi_pb2_grpc

import time

HOST = "grpc.sandbox.iot.enlight.skf.com"
PORT = "50051"

try:
	with open('./cert/ca.crt', mode='rb') as f:
		trusted_certs = f.read()

	with open('./cert/client.crt', mode='rb') as f:
		client_cert = f.read()

	with open('./cert/client.key', mode='rb') as f:
		client_key = f.read()
except Exception as e:
	log.error('failed-to-read-cert-keys', reason=e)

credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs, private_key=client_key, certificate_chain=client_cert)
channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), credentials)
stub = grpcapi_pb2_grpc.IoTStub(channel)

data = grpcapi_pb2.NodeData(created_at = int(round(time.time() * 1000)),
							content_type = 6,
							question_answers = ['Yes'])


stub.IngestNodeData(grpcapi_pb2.IngestNodeDataInput(node_id='4607e63a-652e-4009-b93c-c00fb4443a13', node_data=data))

channel.close()
