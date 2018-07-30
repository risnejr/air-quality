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

    def __init__(self, asset, csv_file, model_name='model_weights.h5'):
        self.x = np.zeros((1, 4))
        self.asset = asset
        self.csv_file = csv_file
        self.model_name = model_name
        self.asset_ids_completed = False
        self.classes = ['Good', 'Ok', 'Bad']
        self.answers = {'Good': np.array([[1, 0, 0]]),
                        'Ok':   np.array([[0, 1, 0]]),
                        'Bad':  np.array([[0, 0, 1]])}

        self.read_ids()
        self.define_model()
        self.grpc_stream()

    def read_ids(self):
        self.node_ids = defaultdict(dict)

        with open(self.csv_file, 'r') as f:
            next(f)
            for row in csv.reader(f, skipinitialspace=True, delimiter=','):
                if len(row) == 3:
                    self.node_ids[row[0]].update({row[1]: row[2]})

    def asset_ids(self):
        try:
            self.node_ids = dict(self.node_ids)
            self.node_ids = self.node_ids[self.asset]
            self.asset_ids_completed = True
        except KeyError as e:
            print('Asset {} does not exist'.format(e))
            raise

    def run(self, data):
        if not self.asset_ids_completed:
            self.asset_ids()
        try:
            if data.node_id == self.node_ids['vote']:
                y_true = self.answers[data.node_data.question_answers[0]]
                self.x = normalize(self.x)
                self.train(y_true)

            if data.node_id == self.node_ids['temp']:
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
                    data = grpcapi_pb2.NodeData(created_at=int(round(time.time() * 1000)),
                                                content_type=6,
                                                question_answers=[self.classes[np.argmax(y_pred)]])
                    self.stub.IngestNodeData(grpcapi_pb2.IngestNodeDataInput(node_id=self.node_ids['pred'],
                                                                             node_data=data))
        except KeyError as e:
            print('Asset is missing key {}'.format(e))
            raise

    def define_model(self):
        self.model = Sequential()
        self.model.add(Dense(32, activation='relu', input_shape=(4,)))
        self.model.add(Dense(3, activation='softmax'))
        adam = Adam()
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=adam,
                           metrics=['accuracy'])

        try:
            self.model.load_weights(self.model_name)
        except IOError:
            print('No file named {}'.format(self.model_name))

    def train(self, y):
        self.model.fit(self.x, y, epochs=1)

    def predict(self):
        return self.model.predict(self.x)

    def grpc_stream(self):
        self.channel = dial_grpc.dial()
        self.stub = grpcapi_pb2_grpc.IoTStub(self.channel)
        self.stub.DeepPing(grpcapi_pb2.PrimitiveVoid())
        self.response = self.stub.GetNodeDataStream(grpcapi_pb2.
                                                    GetNodeDataStreamInput())

    def main(self):
        t0 = time.time()
        for data in self.response:
            self.run(data)
            if time.time() - t0 > 60:
                self.model.save_weights(self.model_name)
                t0 = time.time()

        self.channel.close()
