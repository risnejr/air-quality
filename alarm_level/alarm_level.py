import alarm_level.dial_grpc as dial_grpc
import alarm_level.grpcapi_pb2 as grpcapi_pb2
import alarm_level.grpcapi_pb2_grpc as grpcapi_pb2_grpc

import numpy as np
import time
import csv

from collections import defaultdict
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils import normalize

CLASSES = ['Good', 'Ok', 'Bad']
ANSWERS = {'Good': np.array([[1, 0, 0]]),
		   'Ok':   np.array([[0, 1, 0]]),
		   'Bad':  np.array([[0, 0, 1]])}

def get_nodes(csv_file):
	node_id = defaultdict(dict)

	with open(csv_file, 'r') as f:
		for row in csv.reader(f, delimiter=','):
			node_id[row[0]].update({row[1]: row[2]})

	return node_id

def run(data, x, model, node_id):
	if data.node_id == node_id['vote']:
		y_true = ANSWERS[data.node_data.question_answers[0]]
		x = normalize(x)
		model = update_weights(x, y_true, model)
	elif data.node_id == node_id['temp']:
		x[0, 0] = data.node_data.data_point.coordinate.y
	elif data.node_id == node_id['pres']:
		x[0, 1] = data.node_data.data_point.coordinate.y
	elif data.node_id == node_id['hum']:
		x[0, 2] = data.node_data.data_point.coordinate.y
	elif data.node_id == node_id['gas']:
		x[0, 3] = data.node_data.data_point.coordinate.y
		if x.all():
			x = normalize(x)
			y_pred = predict_level(x, model)
			print(CLASSES[np.argmax(y_pred)], y_pred)

	return x, model


def define_network():
	model = Sequential()
	model.add(Dense(32, activation='relu', input_shape=(4,)))
	model.add(Dense(3, activation='softmax'))

	adam = Adam()
	model.compile(loss='categorical_crossentropy',
				  optimizer=adam,
				  metrics=['accuracy'])

	try:
		model.load_weights('aq_model_weights.h5')
	except IOError:
		print('No file named aq_model_weights.h5')

	return model

def update_weights(x, y, model):
	model.fit(x, y, epochs=1)

	return model

def predict_level(x, model):
	prediction = model.predict(x)

	return prediction

def grpc_stream():
	channel = dial_grpc.dial()
	stub = grpcapi_pb2_grpc.IoTStub(channel)
	response = stub.GetNodeDataStream(grpcapi_pb2.GetNodeDataStreamInput())

	return response

def main():
	x = np.zeros((1, 4))
	model = define_network()
	response = grpc_stream()
	node_id = get_nodes('node_id.csv')['desk']
	t0 = time.time()

	for data in response:
		x, model = run(data, x, model, node_id)
		if time.time() - t0 > 60:
			print('Saving model...')
			model.save_weights('aq_model_weights.h5')
			t0 = time.time()

	channel.close()
