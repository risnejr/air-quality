import sys
sys.path.append('./proto')

import grpc
import grpcapi_pb2
import grpcapi_pb2_grpc

import datetime
import matplotlib.pyplot as plt
import seaborn as sns

HOST = "grpc.sandbox.iot.enlight.skf.com"
PORT = "50051"

QUALITY = "e8e1e003-ae83-4a7e-8190-c08c36811415"
TEMP_ID = "c52fcf61-3599-404a-9492-0b720a469f22"
QUESTION = "4607e63a-652e-4009-b93c-c00fb4443a13"

TEMP_ID_D = "59959859-2dc6-4689-bf24-fda966cb4012"

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

# response = stub.GetNodeData(grpcapi_pb2.GetNodeDataInput(node_id=TEMP_ID))
response = stub.GetNodeDataStream(grpcapi_pb2.GetNodeDataStreamInput())

while True:
	output = response.next()
	if output.node_id == TEMP_ID:
		print(output.node_data.data_point.coordinate)

# y = []
# for node_data in response.node_data_list:
# 	y.append(node_data.data_point.coordinate.y)

# plt.plot(y)
# plt.show()

# print(response.node_data_list[-1].data_point.coordinate.y)
# print(datetime.datetime.fromtimestamp(round(response.node_data_list[-1].data_point.coordinate.x/1000)).strftime('%Y-%m-%d %H:%M:%S'))
# print(response)

channel.close()
