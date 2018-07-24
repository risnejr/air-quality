# Alarm Levels
This is a repository for user generated alarm levels in an office environment using data collected with a **RPi** and a **BME680** sensor.
## Required files
```
.
├── alarm_level.py
├── cert
│   ├── ca.crt
│   ├── client.crt
│   └── client.key
├── dial_grpc.py
├── node_id.csv
└── proto
    └── grpcapi.proto
```
## How to generate code from proto files
```
python3 -m pip install --user grpcio-tools
python3 -m grpc_tools.protoc -I ./alarm_level/proto --python_out=./alarm_level --grpc_python_out=./alarm_level ./alarm_level/proto/grpcapi.proto`
```
