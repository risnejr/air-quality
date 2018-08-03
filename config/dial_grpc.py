import grpc


def dial():
    HOST = 'grpc.sandbox.hierarchy.enlight.skf.com'
    PORT = '50051'
    CERT = '../certs/hierarchy/'

    try:
        with open(CERT + 'ca.crt', mode='rb') as f:
            trusted_certs = f.read()

        with open(CERT + 'client.crt', mode='rb') as f:
            client_cert = f.read()

        with open(CERT + 'client.key', mode='rb') as f:
            client_key = f.read()
    except Exception as e:
        print('failed-to-read-cert-keys', e)

    credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs,
                                               private_key=client_key,
                                               certificate_chain=client_cert)
    channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), credentials)

    return channel
