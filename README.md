# Alarm Levels
This is a repository for user generated alarm levels in an office environment using data collected with a **RPi** and a **BME680** sensor.
## Required files
```
.
├── alarm_level
│   ├── __init__.py
│   ├── alarm_level.py
│   ├── cert                <---- 
│   │   ├── ca.crt
│   │   ├── client.crt
│   │   └── client.key
│   ├── dial_grpc.py
│   ├── grpcapi_pb2.py
│   ├── grpcapi_pb2_grpc.py
│   └── proto
│       └── grpcapi.proto
├── main.py
└── node_ids.csv            <---- 
```
## Generate code from proto files
```
python3 -m pip install --user grpcio-tools
python3 -m grpc_tools.protoc -I ./alarm_level/proto --python_out=./alarm_level --grpc_python_out=./alarm_level ./alarm_level/proto/grpcapi.proto
```
## Run unit tests
```
python3 -m unittest discover -v
```
