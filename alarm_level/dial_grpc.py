import grpc

import alarm_level.grpcapi_pb2 as grpcapi_pb2
import alarm_level.grpcapi_pb2_grpc as grpcapi_pb2_grpc

def dial():
	HOST = "grpc.sandbox.iot.enlight.skf.com"
	PORT = "50051"

	try:
		with open('alarm_level/cert/ca.crt', mode='rb') as f:
			trusted_certs = f.read()

		with open('alarm_level/cert/client.crt', mode='rb') as f:
			client_cert = f.read()

		with open('alarm_level/cert/client.key', mode='rb') as f:
			client_key = f.read()
	except Exception as e:
		print('failed-to-read-cert-keys', e)

	credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs, private_key=client_key, certificate_chain=client_cert)
	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), credentials)

	return channel
