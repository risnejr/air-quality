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
	def __init__(self, function_loc, csv_file):
		self.x = np.zeros((1, 4))
		self.model = Sequential()
		self.csv_file = csv_file
		self.location = function_loc
		self.node_ids = defaultdict(dict)
		self.csv_file = csv_file
		self.classes = ['Good', 'Ok', 'Bad']
		self.answers = {'Good': np.array([[1, 0, 0]]),
						'Ok':   np.array([[0, 1, 0]]),
						'Bad':  np.array([[0, 0, 1]])}

	def read_node_ids(self):
		with open(self.csv_file, 'r') as f:
			header = next(f)
			for row in csv.reader(f, skipinitialspace=True ,delimiter=','):
				if len(row) == 3:
					self.node_ids[row[0]].update({row[1]: row[2]})

		try:
			self.node_ids = dict(self.node_ids)
			self.node_ids = self.node_ids[self.location]
		except KeyError:
			raise


	def run(self, data):
		if data.node_id == self.node_ids['vote']:
			y_true = self.answers[data.node_data.question_answers[0]]
			self.x = normalize(self.x)
			self.train(y_true)

		elif data.node_id == self.node_ids['temp']:
			self.x[0, 0] = data.node_data.data_point.coordinate.y

		elif data.node_id == self.node_ids['pres']:
			self.x[0, 1] = data.node_data.data_point.coordinate.y

		elif data.node_id == self.node_ids['hum']:
			self.x[0, 2] = data.node_data.data_point.coordinate.y

		elif data.node_id == self.node_ids['gas']:
			self.x[0, 3] = data.node_data.data_point.coordinate.y
			if self.x.all():
				self.x = normalize(self.x)
				y_pred = self.predict()
				print(self.classes[np.argmax(y_pred)], y_pred)

	def define_model(self):
		self.model.add(Dense(32, activation='relu', input_shape=(4,)))
		self.model.add(Dense(3, activation='softmax'))
		adam = Adam()
		self.model.compile(loss='categorical_crossentropy',
					optimizer=adam,
					metrics=['accuracy'])

		try:
			self.model.load_weights('aq_model_weights.h5')
		except IOError:
			print('No file named aq_model_weights.h5')

	def train(self, y):
		self.model.fit(self.x, y, epochs=1)

	def predict(self):
		return self.model.predict(self.x)

	def grpc_stream(self):
		channel = dial_grpc.dial()
		stub = grpcapi_pb2_grpc.IoTStub(channel)
		response = stub.GetNodeDataStream(grpcapi_pb2.GetNodeDataStreamInput())

		return response

	def main(self):
		t0 = time.time()
		self.define_model()
		self.read_node_ids()
		response = self.grpc_stream()

		for data in response:
			print(data)
			self.run(data)
			if time.time() - t0 > 60:
				print('Saving model...')
				self.model.save_weights('aq_model_weights.h5')
				t0 = time.time()

		channel.close()
