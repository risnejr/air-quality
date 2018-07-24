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

class AlarmLevel:
	def __init__(self, function_loc):
		self.location = function_loc
		self.classes = ['Good', 'Ok', 'Bad']
		self.answers = {'Good': np.array([[1, 0, 0]]),
						'Ok':   np.array([[0, 1, 0]]),
						'Bad':  np.array([[0, 0, 1]])}

	def get_node_ids(self, csv_file):
		node_ids = defaultdict(dict)

		with open(csv_file, 'r') as f:
			header = next(f)
			for row in csv.reader(f, delimiter=','):
				node_ids[row[0]].update({row[1]: row[2]})

		return node_ids

	def run(self, data, x, model, node_ids):
		if data.node_id == node_ids['vote']:
			y_true = self.answers[data.node_data.question_answers[0]]
			x = normalize(x)
			model = self.train(x, y_true, model)
		elif data.node_id == node_ids['temp']:
			x[0, 0] = data.node_data.data_point.coordinate.y
		elif data.node_id == node_ids['pres']:
			x[0, 1] = data.node_data.data_point.coordinate.y
		elif data.node_id == node_ids['hum']:
			x[0, 2] = data.node_data.data_point.coordinate.y
		elif data.node_id == node_ids['gas']:
			x[0, 3] = data.node_data.data_point.coordinate.y
			if x.all():
				x = normalize(x)
				y_pred = self.predict(x, model)
				print(self.classes[np.argmax(y_pred)], y_pred)

		return x, model


	def define_model(self):
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

	def train(self, x, y, model):
		model.fit(x, y, epochs=1)

		return model

	def predict(self, x, model):
		return model.predict(x)

	def grpc_stream(self):
		channel = dial_grpc.dial()
		stub = grpcapi_pb2_grpc.IoTStub(channel)
		response = stub.GetNodeDataStream(grpcapi_pb2.GetNodeDataStreamInput())

		return response

	def main(self):
		x = np.zeros((1, 4))
		model = self.define_model()
		response = self.grpc_stream()
		node_ids = self.get_node_ids('node_id.csv')[self.location]
		t0 = time.time()

		for data in response:
			x, model = self.run(data, x, model, node_ids)
			if time.time() - t0 > 60:
				print('Saving model...')
				model.save_weights('aq_model_weights.h5')
				t0 = time.time()

		channel.close()
